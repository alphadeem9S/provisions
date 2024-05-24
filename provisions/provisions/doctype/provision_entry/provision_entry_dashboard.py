from frappe import _


def get_data():
	return {
		"fieldname": "provision_entry",
		"non_standard_fieldnames": {
			"Journal Entry": "reference_name",
			"Payment Entry": "reference_name",
		},
		"transactions": [{"label": _("Journal Entry"), "items": ["Journal Entry"]}],
	}
