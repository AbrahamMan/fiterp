# -*- coding: utf-8 -*-
# Copyright (c) 2018, ITKMITL and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname
from erpnext.hr.utils import set_employee_name
#from erpnext.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
#from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
#from erpnext.hr.doctype.employee_leave_approver.employee_leave_approver import get_approver_list


class LeaveApplicationfiterp(Document):
	pass


def validate(self, func):
	if not getattr(self, "__islocal", None) and frappe.db.exists(self.doctype, self.name):
		self.previous_doc = frappe.get_value(self.doctype, self.name, "leave_approver", as_dict=True)
	else:
		self.previous_doc = None

	set_employee_name(self)

	self.validate_dates()
	self.validate_balance_leaves()
#	self.validate_leave_overlap()
	validate_leave_overlap(self)
	self.validate_max_days()
	self.show_block_day_warning()
	self.validate_block_days()
	self.validate_salary_processed_days()
	#	#self.validate_leave_approver()
	self.validate_attendance()


	if (self.workflow_state == "Applied" and self.approver_1_email != "-n/a-"):
		self.leave_approver = self.approver_1_email

	if (self.workflow_state == "Approved by Supervisor" and self.approver_2_email != "-n/a-"):
		self.leave_approver = self.approver_2_email
	if (self.workflow_state == "Approved by Senior Mgr" and self.approver_3_email != "-n/a-"):
		self.leave_approver = self.approver_3_email

	if (self.workflow_state == "Approved"): 
		self.status = "Approved"
	if (self.workflow_state == "Rejected"): 
		self.status = "Rejected"
	if (self.workflow_state == "Cancelled"): 
		self.status = "Open"

####

def on_update(self, func):
	#custom code : 6 Jan 2018
	self.notify_leave_approver()

def on_submit(self, func):
	if self.status == "Open":
		frappe.throw(_("Only Leave Applications with status 'Approved' and 'Rejected' can be submitted"))

	self.validate_back_dated_application()

	# notify leave applier about approval
	#self.notify_employee(self.status)
	self.notify_employee(self.workflow_state)

def on_cancel(self, func):
	# notify leave applier about cancellation
	self.notify_employee("cancelled")


def validate_leave_overlap(self):
	if not self.name:
		# hack! if name is null, it could cause problems with !=
		self.name = "New Leave Application"

	for d in frappe.db.sql("""
		select
			name, leave_type, posting_date, from_date, to_date, total_leave_days, half_day_date, half_day_am, half_day_pm 
		from `tabLeave Application`
		where employee = %(employee)s and docstatus < 2 and status in ("Open", "Approved")
		and to_date >= %(from_date)s and from_date <= %(to_date)s
		and name != %(name)s""", {
			"employee": self.employee,
			"from_date": self.from_date,
			"to_date": self.to_date,
			"name": self.name
		}, as_dict = 1):

		if cint(self.half_day)==1 and getdate(self.half_day_date) == getdate(d.half_day_date) and (
			flt(self.total_leave_days)==0.5
			or getdate(self.from_date) == getdate(d.to_date)
			or getdate(self.to_date) == getdate(d.from_date)):

			total_leaves_on_half_day = self.get_total_leaves_on_half_day()
			if total_leaves_on_half_day >= 1:
				self.throw_overlap_error(d)
#custom code
		elif (cint(self.half_day_pm) == 1 or cint(self.half_day_am) == 1) and cint(self.half_day_am)*cint(self.half_day_pm) == 0:
			total_leaves_on_half_day = 1
			if cint(self.half_day_pm) == 1 and (getdate(self.from_date) == getdate(d.to_date)) and cint(d.half_day_am) == 1: 
				total_leaves_on_half_day = 0.5
			if cint(self.half_day_am) == 1 and (getdate(self.to_date) == getdate(d.from_date)) and cint(d.half_day_pm) == 1: 
				total_leaves_on_half_day = 0.5
				
			if total_leaves_on_half_day >= 1:
				self.throw_overlap_error(d)

			#getdate(self.from_date) == getdate(d.to_date)
			#self.throw_overlap_error(d)
#custom code end
		else:
			self.throw_overlap_error(d)

#custom code
def get_half_day_pm(self, func):
	leave_count_on_half_day_date = frappe.db.sql("""select count(name) from `tabLeave Application`
		where employee = %(employee)s
		and docstatus < 2
		and status in ("Open", "Approved")
		and ((half_day_pm = 1) or (half_day_pm = 0 and half_day_am = 0))
		and half_day_date = %(half_day_date)s
		and name != %(name)s""", {
			"employee": self.employee,
			"half_day_date": self.from_date,
			"name": self.name
		})[0][0]
	return leave_count_on_half_day_date

def get_half_day_am(self, func):
	leave_count_on_half_day_date = frappe.db.sql("""select count(name) from `tabLeave Application`
		where employee = %(employee)s
		and docstatus < 2
		and status in ("Open", "Approved")
		and ((half_day_am = 1) or (half_day_pm = 0 and half_day_am = 0))
		and half_day_date = %(half_day_date)s
		and name != %(name)s""", {
			"employee": self.employee,
			"half_day_date": self.to_date,
			"name": self.name
		})[0][0]
	return leave_count_on_half_day_date

#custom code end


@frappe.whitelist()
#def get_number_of_leave_days(employee, leave_type, from_date, to_date, half_day = None, half_day_date = None):
def get_number_of_leave_days(employee, leave_type, from_date, to_date, half_day = None, half_day_date = None, half_day_pm = None, half_day_am = None):
	number_of_days = 0
	if half_day == 1:
		if from_date == to_date:
			number_of_days = 0.5
		else:
			number_of_days = date_diff(to_date, from_date) + .5
	elif (cint(half_day_am) == 1 or cint(half_day_pm) == 1):
		if from_date == to_date:
			number_of_days = (cint(half_day_am) + cint(half_day_pm))*0.5
		else:
			number_of_days = date_diff(to_date, from_date) - (cint(half_day_am) + cint(half_day_pm))*0.5 + 1
			#number_of_days = date_diff(to_date, from_date) - 1 + 1
		
	else:
		number_of_days = date_diff(to_date, from_date) + 1

	if not frappe.db.get_value("Leave Type", leave_type, "include_holiday"):
		number_of_days = flt(number_of_days) - flt(get_holidays(employee, from_date, to_date))
	return number_of_days



