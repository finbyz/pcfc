// Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt
frappe.ui.form.on('Dubai Maritime City Authority', {
	refresh(frm) {
	if (!frm.doc.agent_name && frm.doc.__islocal){
	    frm.set_value("agent_name",frappe.session.user);
	}
	if (!frm.doc.business_unit && frm.doc.__islocal){
	    frm.set_value("business_unit",frm.doc.doctype);
	}
	}
})
cur_frm.fields_dict.sub_service_type.get_query = function(doc) {
	return {
		filters: {
			"service_type": doc.service_type
		}
	}
};