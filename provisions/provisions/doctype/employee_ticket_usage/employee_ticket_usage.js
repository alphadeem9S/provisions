// Copyright (c) 2023, Peter Maged and contributors
// For license information, please see license.txt

let fields_to_refresh =[
	'total_tickets' ,
	'ticket_rate' ,
	'total_amount' ,
]
frappe.ui.form.on("Employee Ticket Usage", {
  // refresh: function(frm) {

  // }

  set_totals: function (frm) {
    frm.call({
      method: "get_total_ticket_amount",
      doc: frm.doc,
      callback: function (r) {
        frm.refresh_fields(fields_to_refresh);
      },
    });
  },
  total_tickets: function (frm) {
    frm.events.set_totals(frm);
  },
});
