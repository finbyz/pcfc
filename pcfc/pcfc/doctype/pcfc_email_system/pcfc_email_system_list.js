frappe.listview_settings['PCFC Email System'] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		return [__(doc.status), {
			"New": "red",
			"Assigned to Call Center Team": "purple",
			"Assigned to BU Focal Points": "yellow",	
			"Resolved": "green"
		}[doc.status], "status,=," + doc.status];
	}
};