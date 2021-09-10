// Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.listview_settings['Dubai Maritime City Authority'] = {
	add_fields: ["case_status"],
	get_indicator: function (doc) {
		return [__(doc.case_status), {
			"Open": "red",
			"Forwarded to DMCA": "lightblue",
			"Resolved": "orange",				
			"In Progress": "green"
		}[doc.case_status], "status,=," + doc.case_status];
	}
};