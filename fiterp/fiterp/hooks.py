# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "fiterp"
app_title = "Fiterp"
app_publisher = "ITKMITL"
app_description = "An ERP application for the faculty of IT, KMITL."
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "erp@it.kmitl.ac.th"
app_license = "MIT"
fixtures=["Custom Field"]
fixtures=["Custom Script"]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/fiterp/css/fiterp.css"
# app_include_js = "/assets/fiterp/js/fiterp.js"

# include js, css files in header of web template
# web_include_css = "/assets/fiterp/css/fiterp.css"
# web_include_js = "/assets/fiterp/js/fiterp.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "fiterp.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "fiterp.install.before_install"
# after_install = "fiterp.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fiterp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
 	"Leave Application": {
 		"validate": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.validate",
 		"on_update": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.on_update",
 		"on_submit": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.on_submit",
 		"on_cancel": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.on_cancel",
# 		"validate_dates": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.validate_dates",
# 		"validate_leave_overlap": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.validate_leave_overlap",
# 		"get_total_leaves_on_half_day": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.get_total_leaves_on_half_day",
# 		"get_half_day_pm": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.get_half_day_pm",
# 		"get_half_day_am": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.get_half_day_am",
# 		"get_number_of_leave_days": "fiterp.fiterp.doctype.leave_application_fiterp.leave_application_fiterp.get_number_of_leave_days",
	}
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"fiterp.tasks.all"
# 	],
# 	"daily": [
# 		"fiterp.tasks.daily"
# 	],
# 	"hourly": [
# 		"fiterp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"fiterp.tasks.weekly"
# 	]
# 	"monthly": [
# 		"fiterp.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "fiterp.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "fiterp.event.get_events"
# }

