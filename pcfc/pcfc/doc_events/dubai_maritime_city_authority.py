# -*- coding: utf-8 -*-
# Copyright (c) 2021, Finbyz Tech. Pvt. Ltd. and contributors
# For license information, please see license.txt
import re
import frappe

def validate(self,method):
    emirates_validation(self)

def emirates_validation(self):
    # validate the format xxx-xxxx-xxxxxxx-x (Emirates ID)"784-1980-1234567-9"
    regex = '^784-[0-9]{4}-[0-9]{7}-[0-9]{1}'
    if re.match(regex,self.emirates_id,flags=0)==None:
        frappe.throw("Emirates ID is not in proper format. Required Format 784-XXXX-XXXXXXX-X")
    
