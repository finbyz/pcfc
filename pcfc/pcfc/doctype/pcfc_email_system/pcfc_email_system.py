# Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, now_datetime, getdate, get_weekdays, add_to_date, get_time, get_datetime, time_diff_in_seconds

class PCFCEmailSystem(Document):
	def validate(self):
		if not self.raised_by:
			self.raised_by = frappe.session.user
		self.update_status()
		#self.agent_response_area =  frappe.render_template(self.agent_response_area, self)

	def update_status(self):
		status = frappe.db.get_value("Issue", self.name, "status")
		# if self.status != "Open" and status == "Open" and not self.first_responded_on:
		# 	self.first_responded_on = frappe.flags.current_time or now_datetime()

		if self.status in ["Closed", "Resolved"] and status not in ["Resolved", "Closed"]:
			self.resolution_date = frappe.flags.current_time or now_datetime()
			
			set_resolution_time(issue=self)
			#set_user_resolution_time(issue=self)

		if self.status == "Open" and status != "Open":
			# if no date, it should be set as None and not a blank string "", as per mysql strict config
			self.resolution_date = None
			self.reset_issue_metrics()
			
	def reset_issue_metrics(self):
		self.db_set("resolution_time", None)

def set_resolution_time(issue):
	# total time taken from issue creation to closing
	resolution_time = time_diff_in_seconds(issue.resolution_date, issue.creation)
	issue.db_set("resolution_time", resolution_time)
