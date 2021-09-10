# Copyright (c) 2021, Finbyz Tech. Pvt. Ltd. and contributors
# For license information, please see license.txt
import re
import frappe
from frappe import _
from frappe.email.doctype.notification.notification import get_context
def validate(self,method):
    get_emailid(self)

def get_emailid(self):
    if self.email_address=="test@test.com":
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
