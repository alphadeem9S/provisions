
from frappe import _


def get_data(data={}):
    data["non_standard_fieldnames"] = {
        "Journal Entry": "reference_name",
    }
    data['transactions'].append(
        {'label': _('Journal Entry'),
         'items': ['Journal Entry']
         }
    )
    return data
    return {
        'fieldname': 'leave_application',
        'transactions': [
            {
                'items': ['Attendance']
            }
        ],
        'reports': [
            {
                'label': _('Reports'),
                'items': ['Employee Leave Balance']
            }
        ]
    }
