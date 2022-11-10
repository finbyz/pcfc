from __future__ import unicode_literals
import frappe
import datetime

from frappe import sendmail, msgprint, db, _
from frappe.core.doctype.role.role import get_info_based_on_role
from frappe.utils import validate_email_address, split_emails

def get_list_of_recipients(self, doc, context):
	recipients = []
	cc = []
	bcc = []
	for recipient in self.recipients:
		if recipient.condition:
			if not frappe.safe_eval(recipient.condition, None, context):
				continue
		if recipient.receiver_by_document_field:
			fields = recipient.receiver_by_document_field.split(',')
			# fields from child table
			if len(fields) > 1:
				for d in doc.get(fields[1]):
					email_id = d.get(fields[0])
					if validate_email_address(email_id):
						recipients.append(email_id)
			# field from parent doc
			else:
				email_ids_value = doc.get(fields[0])
				if validate_email_address(email_ids_value):
					email_ids = email_ids_value.replace(",", "\n")
					recipients = recipients + email_ids.split("\n")

		if recipient.cc and "{" in recipient.cc:
			recipient.cc = frappe.render_template(recipient.cc, context)

		if recipient.cc:
			recipient.cc = recipient.cc.replace(",", "\n")
			cc = cc + recipient.cc.split("\n")

		if recipient.bcc and "{" in recipient.bcc:
			recipient.bcc = frappe.render_template(recipient.bcc, context)

		if recipient.bcc:
			recipient.bcc = recipient.bcc.replace(",", "\n")
			bcc = bcc + recipient.bcc.split("\n")

		#For sending emails to specified role
		if recipient.receiver_by_role:
			emails = get_info_based_on_role(recipient.receiver_by_role, 'email')

			for email in emails:
				recipients = recipients + email.split("\n")

	if self.send_to_all_assignees:
		recipients = recipients + get_assignees(doc)
	# Finbyz Changes for replace cc with recipients
	return list(set(cc)), [], list(set(recipients))

def validate(self,method):
	get_emailid(self)
	
def get_emailid(self):
	email=frappe.db.get_all('Email Condition',filters={'doctype_name':['=',self.doctype]})
	for each in email:
		doc=frappe.get_doc('Email Condition',each)
		if validate_condition(self,doc.condition):
			self.email_id = doc.email_id

def validate_condition(self,condition):
	temp_doc = frappe.new_doc(self.doctype)
	if condition:
		try:
			frappe.safe_eval(condition, None, get_context(temp_doc.as_dict()))
			return True
		except Exception:
			return False

def create_new_parent(self, communication, email):
	'''If no parent found, create a new reference document'''

	# no parent found, but must be tagged
	# insert parent type doc
	parent = frappe.new_doc(self.append_to)

	if self.subject_field:
		parent.set(self.subject_field, frappe.as_unicode(email.subject)[:140])

	if self.sender_field:
		parent.set(self.sender_field, frappe.as_unicode(email.from_email))

	if parent.meta.has_field("email_account"):
		parent.email_account = self.name

	# finbyz change start
	if parent.meta.has_field("to"):
		recipients = ''
		# validate recipients
		if communication.recipients and communication.recipients.find(""", IBT" <""") != -1:
			communication.recipients = communication.recipients.replace(""", IBT" <""",""" IBT" <""")
		for email in split_emails(communication.recipients):
			if not recipients:
				recipients = validate_email_address(email, throw=True)
			else:
				recipients = recipients + ', ' + validate_email_address(email, throw=True)
		parent.to = recipients

	if parent.meta.has_field("cc"):
		cc = ''
		# validate CC
		if communication.cc and communication.cc.find(""", IBT" <""") != -1:
			communication.cc = communication.cc.replace(""", IBT" <""",""" IBT" <""")
		for email in split_emails(communication.cc):
			if not cc:
				cc = validate_email_address(email, throw=True)
			else:
				cc = cc + ', ' + validate_email_address(email, throw=True)
		parent.cc = cc
	# finbyz change end
	parent.flags.ignore_mandatory = True

	try:
		parent.insert(ignore_permissions=True)
	except frappe.DuplicateEntryError:
		# try and find matching parent
		parent_name = frappe.db.get_value(self.append_to, {self.sender_field: email.from_email})
		if parent_name:
			parent.name = parent_name
		else:
			parent = None

	# NOTE if parent isn't found and there's no subject match, it is likely that it is a new conversation thread and hence is_first = True
	communication.is_first = True

	return parent

from frappe.core.utils import get_parent_doc
from frappe.automation.doctype.assignment_rule.assignment_rule import apply as apply_assignment_rule
from frappe.core.doctype.communication.communication import update_first_response_time, set_avg_response_time

def update_parent_document_on_communication(doc):
	"""Update mins_to_first_communication of parent document based on who is replying."""

	parent = get_parent_doc(doc)
	if not parent:
		return

	# update parent mins_to_first_communication only if we create the Email communication
	# ignore in case of only Comment is added
	if doc.communication_type == "Comment":
		return

	status_field = parent.meta.get_field("status")
	if status_field:
		options = (status_field.options or "").splitlines()

		# if status has a "Replied" option, then update the status for received communication
		# finbyz changes
		if (("Replied" in options) or ("Assigned to Call Center Team" in options)) and doc.sent_or_received == "Received":
			if ("Assigned to Call Center Team" in options):
				parent.db_set("status", "New")
			else:
				parent.db_set("status", "Open")
			parent.run_method("handle_hold_time", "Replied")
			apply_assignment_rule(parent)
		else:
			# update the modified date for document
			parent.update_modified()

	update_first_response_time(parent, doc)
	set_avg_response_time(parent, doc)
	parent.run_method("notify_communication", doc)
	parent.notify_update()

def comm_before_validate(self,method):
	if self.recipients and self.recipients.find(""", IBT" <""") != -1:
		self.recipients = self.recipients.replace(""", IBT" <""",""" IBT" <""")

	if self.cc and self.cc.find(""", IBT" <""") != -1:
		self.cc = self.cc.replace(""", IBT" <""",""" IBT" <""")

	if self.bcc and self.bcc.find(""", IBT" <""") != -1:
		self.bcc = self.bcc.replace(""", IBT" <""",""" IBT" <""")