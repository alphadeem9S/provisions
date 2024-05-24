// Copyright (c) 2023, Peter Maged and contributors
// For license information, please see license.txt

frappe.ui.form.on("Provisions Settings", {
  // refresh: function(frm) {

  // },
  setup: function (frm) {
    frm.set_query("end_of_service_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("end_of_service_operation_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("end_of_service_provision_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("tickets_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("tickets_operation_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("tickets_provision_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("leaves_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("leaves_operation_expense_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("leaves_provision_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("end_of_service_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("end_of_service_expense_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("tickets_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("tickets_expense_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("leaves_expense_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
    frm.set_query("leaves_cost_center", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
  },
});
