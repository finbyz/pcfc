# Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
from frappe.utils import cint, now_datetime, getdate, get_weekdays, add_to_date, get_time, get_datetime, time_diff_in_seconds
from frappe.core.doctype.communication.email import make as make_communication
from frappe.desk.form.load import get_attachments
import json

class PCFCEmailSystem(Document):
	def validate(self):
		if not self.raised_by and frappe.session.user != "Administrator":
			self.raised_by = frappe.session.user
		self.update_status()
		self.set_status_history()
		self.set_total_duration()
	
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

	def set_status_history(self):
		status = frappe.db.get_value("PCFC Email System", self.name, "status")
		status_list = list(set([row.status for row in self.status_history]))
		if self.status == "New":
			if "New" not in status_list:
				self.append('status_history',{
					'status': self.status,
					'status_time': self.creation
				})
				return

		if status != self.status:
			self.append('status_history',{
				'status': self.status,
				'status_time': frappe.flags.current_time or now_datetime()
			})

		for idx,row in enumerate(self.status_history[:-1]):
			row.duration = time_diff_in_seconds(self.status_history[idx+1].status_time,self.status_history[idx].status_time)

	def set_total_duration(self):
		if self.status_history:
			new = 0
			call_center_duration = 0
			focal_duration = 0
			total_duration = 0
			for row in self.status_history:
				if row.duration:
					total_duration += row.duration
					if row.status == "Assigned to Call Center Team":
						call_center_duration += row.duration
					if row.status == "Assigned to BU Focal Points":
						focal_duration += row.duration
					if row.status == "New":
						new += row.duration
			self.call_center_team_duration= call_center_duration
			self.bu_focal_points_duration= focal_duration
			self.new_duration = new
			self.total_duration = total_duration

			# 2 days SLA	
			if call_center_duration > 172800:
				self.sla_status = "Overdue Call Center Team"
			elif focal_duration > 172800:
				self.sla_status = "Overdue BU Focal Points"
			else:
				self.sla_status = "Within SLA"

	# Attach old emails with current sending email
	@frappe.whitelist()
	def send_issue_close_email(self,select_attachments):
		if not self.to:
			frappe.throw("Please enter recipient email address")
		if not self.subject:
			frappe.throw("Subject is mandatory to send email")
		if not self.agent_response_area:
			frappe.throw("Agent response area is mandatory to send email")
			
		old_communications = frappe.db.get_all("Communication",{"reference_doctype":self.doctype,"reference_name":self.name},
				["content","sender","communication_date","recipients","cc","subject"],order_by='creation desc',page_length=1)
		message = self.agent_response_area
		message += "<br> <hr> <br>"

		for comm in old_communications:
			message += "<b>From: </b> {}<br>".format(comm.sender)
			message += "<b>Sent: </b> {}<br>".format(comm.communication_date)
			message += "<b>To: </b> {}<br>".format(validate_email_address(comm.recipients))
			if comm.cc:
				message += "<b>Cc: </b> {}<br>".format(validate_email_address(comm.cc))
			message += "<b>Subject: </b> {}<br><br>".format(comm.subject)
			message += comm.content

		make_communication(
			recipients = self.raised_by + ', ' + self.to if self.to else self.raised_by,
			subject = self.subject,
			cc = self.cc,
			bcc = [],
			send_email=1,
			content = message,
			doctype = self.doctype,
			name = self.name,
			attachments= select_attachments
		)

		make_communication(doctype=self.doctype,
			name=self.name,
			content=message,
			subject=self.subject,
			recipients=self.raised_by + ', ' + self.to if self.to else self.raised_by,
			communication_medium="Email",
			send_email=False,
			cc=self.cc,
			bcc=[],
			communication_type='Automated Message',
			attachments= select_attachments,
			ignore_permissions=True)

def set_resolution_time(issue):
	# total time taken from issue creation to closing
	resolution_time = time_diff_in_seconds(issue.resolution_date, issue.creation)
	issue.db_set("resolution_time", resolution_time)

