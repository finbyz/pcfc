// Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inquiry and Feedback', {
	refresh(frm) {
		if (!frm.doc.agent_name && frm.doc.__islocal){
			frm.set_value("agent_name",frappe.session.user);
		}
	}
});