from . import __version__ as app_version

app_name = "pcfc"
app_title = "Pcfc"
app_publisher = "Finbyz Tech Pvt Ltd"
app_description = "Custom App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@finbyz.com"
app_license = "GPL 3.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pcfc/css/pcfc.css"
# app_include_js = "/assets/pcfc/js/pcfc.js"

# include js, css files in header of web template
# web_include_css = "/assets/pcfc/css/pcfc.css"
# web_include_js = "/assets/pcfc/js/pcfc.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pcfc/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pcfc.install.before_install"
# after_install = "pcfc.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pcfc.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Dubai Maritime City Authority":{
		"validate":"pcfc.pcfc.doc_events.dubai_maritime_city_authority.validate"
	},
	"Trakhees":{
		"validate":"pcfc.pcfc.doc_events.trakhees.validate"
	},
	"Communication":{
		"before_validate":"pcfc.api.comm_before_validate"
	},
	# ('Dubai Maritime City Authority','Dubai Ports Authority','EHS','Inquiry and Feedback','Marine Agency','PCFC Investment','PCFC Security','Trakhees'):{
	# 	"validate":"pcfc.api.validate"
	# }
	}

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
# 		"pcfc.tasks.all"
# 	],
# 	"daily": [
# 		"pcfc.tasks.daily"
# 	],
# 	"hourly": [
# 		"pcfc.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pcfc.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pcfc.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pcfc.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pcfc.event.get_events"
# }

# to set To and CC field from email
from frappe.email.doctype.email_account.email_account import EmailAccount
from pcfc.api import create_new_parent
EmailAccount.create_new_parent = create_new_parent

# when reply on email status should be new 
from frappe.core.doctype.communication import communication
from pcfc.api import update_parent_document_on_communication
communication.update_parent_document_on_communication = update_parent_document_on_communication

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pcfc.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pcfc.auth.validate"
# ]

# override for cc_field
# from frappe.email.doctype.notification.notification import Notification
# from pcfc.api import get_list_of_recipients
# Notification.get_list_of_recipients = get_list_of_recipients