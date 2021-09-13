// Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('PCFC Email System', {
	email_template: function(frm){
		if(frm.doc.email_template){
			frappe.call({
				method: 'frappe.email.doctype.email_template.email_template.get_email_template',
				args: {
					template_name: frm.doc.email_template,
					doc: frm.doc,
				},
				callback(r) {
					frm.set_value("subject",r.message.subject)
					frappe.db.get_value("User",frappe.session.user,'email_signature',function(d){
						if(d.email_signature){
							frm.set_value("agent_response_area",r.message.message + d.email_signature)
						}
						else{
							frm.set_value("agent_response_area",r.message.message)
						}
					})
					
				},
			});
		}
	},
	//  set_content: function(frm) {
	// 	const { doctype, docname } = frm;
	// 		message = await localforage.getItem(doctype + docname) || "";
		
	// 	//message += await this.get_signature();

	// 	// const SALUTATION_END_COMMENT = "<!-- salutation-ends -->";
	// 	// if (this.real_name && !message.includes(SALUTATION_END_COMMENT)) {
	// 	// 	this.message = `
	// 	// 		<p>${__('Dear {0},', [this.real_name], 'Salutation in new email')},</p>
	// 	// 		${SALUTATION_END_COMMENT}<br>
	// 	// 		${message}
	// 	// 	`;
	// 	// }

	// 	// if (this.is_a_reply) {
	// 	// 	message += this.get_earlier_reply();
	// 	// }

	// 	frm.set_value("agent_response_area", message);
	// }
});
