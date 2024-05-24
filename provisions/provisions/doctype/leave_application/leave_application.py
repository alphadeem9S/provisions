from provisions.provisions.doctype.provision_entry.provision_entry import get_employee_leave_salary
import frappe
from frappe import _
from frappe.utils.data import get_link_to_form
from dateutil import parser
@frappe.whitelist()
def on_submit_leave_application(self,fun=''):
    if self.status != 'Approved' :
        return
    day_rate = get_day_rate(self)
    amount = day_rate * (self.total_leave_days or 0)
    create_journal_entry(self,amount)



def create_journal_entry(self,total_amount):
    if not getattr (self,"include_in_provision" , 0) :
        return
    
    if not frappe.db.exists("Provisions Settings", self.company):
        frappe.throw(
            _("Please Create Provisions Settings for Company {}").format(self.company))
    settings = frappe.get_doc("Provisions Settings", self.company)
    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.voucher_type = "Journal Entry"
    journal_entry.user_remark = _("Employee Ticket Usage Journal Entry for employee {0} in {1}").format(
       self.employee, self.posting_date
    )
    journal_entry.company = self.company
    journal_entry.posting_date = self.posting_date

    # Leaves

    project , cost_center ,employee_type = frappe.db.get_value("Employee" , self.employee , [
        'project' ,
        'cost_center' ,
        'employee_type'
    ])

    journal_entry.append('accounts', {
        "account": settings.leaves_operation_expense_account if employee_type == "Operation" else settings.leaves_expense_account,
        "credit_in_account_currency": total_amount,
        "exchange_rate": 1,
        "cost_center": cost_center or settings.leaves_expense_cost_center,
        "project":project,
        "reference_type": self.doctype,
        "reference_name": self.name,
    })

    # Tickets

    journal_entry.append('accounts', {
        "account": settings.leaves_provision_account,
        "debit_in_account_currency": total_amount,
        "exchange_rate": 1,
        "party_type": 'Employee',
        "party": self.employee,
        # "cost_center" : settings.leaves_cost_center,
        "reference_type": self.doctype,
        "reference_name": self.name,
    })


    journal_entry.save(ignore_permissions=True)
    journal_entry.submit()

    lnk = get_link_to_form(journal_entry.doctype, journal_entry.name)
    frappe.msgprint(_("{} {} was Created").format(
        journal_entry.doctype, lnk))

@frappe.whitelist()
def get_day_rate(self):
    start_date = parser.parse(str(self.from_date))
    end_date = parser.parse(str(self.to_date))
    joining_date ,relieving_date = frappe.db.get_value("Employee",self.employee,['date_of_joining' , 'relieving_date'])
    if joining_date :
        joining_date = parser.parse(str(joining_date))
    if relieving_date :
        relieving_date = parser.parse(str(relieving_date))


    total_salary = get_employee_leave_salary(self.employee , start_date , end_date , joining_date ,relieving_date)
    return total_salary / 30
