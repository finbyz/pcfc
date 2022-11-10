// Copyright (c) 2021, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('PCFC Email System', {
	refresh: function(frm){
		const attach = $(cur_frm.fields_dict.select_attachments.wrapper);
		let attachments = frm.get_docinfo().attachments;

		let args = {
			doctype: frm.doctype,
			docname: frm.docname,
			frm: frm,
			folder: 'Home/Attachments',
			on_success: attachment => {
				console.log("success");
				frm.attachments.attachment_uploaded(attachment);
				console.log(attachment);
				render_attachment_rows(frm,attachments,attachment);
			}
		};
		
		$(`
			<label class="control-label">
				${__("Select Attachments")}
			</label>
			<div class='attach-list'></div>
			<p class='add-more-attachments'>
				<button class='btn btn-xs btn-default'>
					${frappe.utils.icon('small-add', 'xs')}&nbsp;
					${__("Add Attachment")}
				</button>
			</p>
		`).appendTo(attach.empty());

		attach
			.find(".add-more-attachments button")
			.on('click', () => new frappe.ui.FileUploader(args));
	
		render_attachment_rows(frm);
	},
	onload: function(frm){
		if(!frm.doc.agent_name){
			frm.set_value("agent_name",frappe.session.user)
		}
		if(!frm.doc.agent_response_area){
			frappe.db.get_value("User",frappe.session.user,'email_signature',function(d){
				if(d.email_signature){
					frm.set_value("agent_response_area","<br>" + d.email_signature)
				}
			})
		}
		
		const attach = $(cur_frm.fields_dict.select_attachments.wrapper);
		let attachments = frm.get_docinfo().attachments;;
		let args = {
			doctype: frm.doctype,
			docname: frm.docname,
			folder: 'Home/Attachments',
			on_success: attachment => {
				frm.attachments.attachment_uploaded(attachment);
				render_attachment_rows(frm,attachments,attachment);
			}
		};
		
		$(`
			<label class="control-label">
				${__("Select Attachments")}
			</label>
			<div class='attach-list'></div>
			<p class='add-more-attachments'>
				<button class='btn btn-xs btn-default'>
					${frappe.utils.icon('small-add', 'xs')}&nbsp;
					${__("Add Attachment")}
				</button>
			</p>
		`).appendTo(attach.empty());

		attach
			.find(".add-more-attachments button")
			.on('click', () => new frappe.ui.FileUploader(args));
	
		render_attachment_rows(frm);
		
	},
	email_template: function(frm){
		if(frm.doc.email_template){
			frappe.call({
				method: 'frappe.email.doctype.email_template.email_template.get_email_template',
				args: {
					template_name: frm.doc.email_template,
					doc: frm.doc,
				},
				callback(r) {
					// frm.set_value("subject",r.message.subject)
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
	send_email: function(frm){
		const selected_attachments =
			$.map($(cur_frm.fields_dict.select_attachments.wrapper).find("[data-file-name]:checked"), function (element) {
				return $(element).attr("data-file-name");
			});
		frm.call({
			method: "send_issue_close_email",
			doc: frm.doc,
			args:{
				select_attachments:selected_attachments
			},
			callback: function() {
				frappe.show_alert({message:__("Email has been sent Successfully"), indicator:'green'});
			}
		})
		frm.set_value('agent_response_area',null);
		frm.refresh_field('agent_response_area')
	},
	before_save: function(frm){
		if(!frm.doc.__islocal && !frm.doc.subject.includes(frm.doc.name)){
			frm.set_value('subject', frm.doc.subject + " : " + frm.doc.name);
		}
	},
});

function render_attachment_rows(frm,attachments,attachment) {
	const select_attachments = cur_frm.fields_dict.select_attachments;
	const attachment_rows = $(select_attachments.wrapper).find(".attach-list");
	if (attachment) {
		attachment_rows.append(get_attachment_row(attachment, true));
	} else {
		let files = [];
		if (attachments && attachments.length) {
			files = files.concat(attachments);
		}
		if (frm) {
			files = files.concat(frm.get_files());
		}

		if (files.length) {
			$.each(files, (i, f) => {
				if (!f.file_name) return;
				if (!attachment_rows.find(`[data-file-name="${f.name}"]`).length) {
					f.file_url = frappe.urllib.get_full_url(f.file_url);
					attachment_rows.append(get_attachment_row(f));
				}
			});
		}
	}
}

function get_attachment_row(attachment, checked) {
	return $(`<p class="checkbox flex">
		<label class="ellipsis" title="${attachment.file_name}">
			<input
				type="checkbox"
				data-file-name="${attachment.name}"
				${checked ? 'checked': ''}>
			</input>
			<span class="ellipsis">${attachment.file_name}</span>
		</label>
		&nbsp;
		<a href="${attachment.file_url}" target="_blank" class="btn-linkF">
			${frappe.utils.icon('link-url')}
		</a>
	</p>`);
}
