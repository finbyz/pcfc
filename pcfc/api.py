from __future__ import unicode_literals
import frappe
import datetime

from frappe import sendmail, msgprint, db, _
from frappe.core.doctype.role.role import get_info_based_on_role
from frappe.utils import validate_email_address

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