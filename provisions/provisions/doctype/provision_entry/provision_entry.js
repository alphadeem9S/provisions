// Copyright (c) 2023, Peter Maged and contributors
// For license information, please see license.txt

let fields_to_refresh = [
  "employees",
  "total_employees",
  "total_salary",
  "total_tickets",
  "total_leave",
];
frappe.ui.form.on("Provision Entry", {
//   refresh: function(frm) {
// 	frm.reload_doc();
//   } ,
  setup: function (frm) {
    let fields = ["department", "employee", "cost_center"];
    fields.forEach((field) => {
      frm.set_query(field, function () {
        return {
          filters: {
            company: frm.doc.company,
          },
        };
      });
    });
    // frm.set_query('employee','employee', function () {
    // 	return {
    // 		filters: {
    // 			company: frm.doc.company,
    // 		},
    // 	};
    // });
  },
  get_details: function (frm) {
    frappe.call({
      method: "get_employee_details",
      doc: frm.doc,
      callback: function (r) {
        frm.refresh_fields(fields_to_refresh);
      },
    });
  },
});
