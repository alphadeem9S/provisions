from frappe import _


def get_data():
	return {
		"fieldname": "employee_ticket_usage",
		"non_standard_fieldnames": {
			"Journal Entry": "reference_name",
			"Payment Entry": "reference_name",
		},
		"transactions": [{"label": _("Journal Entry"), "items": ["Journal Entry"]}],
	}
