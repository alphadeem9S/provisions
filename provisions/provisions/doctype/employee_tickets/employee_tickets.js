// Copyright (c) 2023, Peter Maged and contributors
// For license information, please see license.txt

let fields_to_refresh = ["tickets", "total_tickets", "total_amount"];
frappe.ui.form.on("Employee Tickets", {
  // refresh: function(frm) {

  // }
  set_totals(frm) {
    frappe.call({
      method: "set_totals",
      doc: frm.doc,
      callback: function (r) {
        frm.refresh_fields(fields_to_refresh);
      },
    });
  },
});

frappe.ui.form.on("Employee Tickets Detail", {
  qty(frm, cdt, cdn) {
    frm.events.set_totals(frm);
  },
  rate(frm, cdt, cdn) {
    frm.events.set_totals(frm);
  },
  tickets_add(frm, cdt, cdn) {
    frm.events.set_totals(frm);
  },
  tickets_remove(frm, cdt, cdn) {
    frm.events.set_totals(frm);
  },
});
