# Copyright (c) 2023, Peter Maged and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import get_link_to_form

class EmployeeTicketUsage(Document):
	def validate(self):
		self.get_total_ticket_amount()
	def on_submit(self):
		self.create_journal_entry()
	def create_journal_entry(self):
		if not frappe.db.exists("Provisions Settings", self.company):
			frappe.throw(
				_("Please Create Provisions Settings for Company {}").format(self.company))
		settings = frappe.get_doc("Provisions Settings", self.company)
		journal_entry = frappe.new_doc("Journal Entry")
		journal_entry.voucher_type = "Journal Entry"
		journal_entry.user_remark = _("Employee Ticket Usage Journal Entry for employee {0} in {1}").format(
			self.employee,self.posting_date
		)
		journal_entry.company = self.company
		journal_entry.posting_date = self.posting_date
            # Salaries
		project , cost_center ,employee_type = frappe.db.get_value("Employee" , self.employee , [
			'project' ,
			'cost_center' ,
			'employee_type'
		])

		# Tickets

		journal_entry.append('accounts', {
			"account": settings.tickets_operation_expense_account if employee_type == "Operation" else settings.tickets_expense_account,
			"credit_in_account_currency": self.total_amount,
			"exchange_rate": 1,
			"project":project ,
			"cost_center":cost_center or settings.tickets_cost_center,
			# "cost_center": settings.tickets_expense_cost_center,
			"reference_type": self.doctype,
			"reference_name": self.name,
		})

		# Tickets

		journal_entry.append('accounts', {
			"account": settings.tickets_provision_account,
			"debit_in_account_currency": self.total_amount,
			# "cost_center":settings.tickets_cost_center,
			
			"exchange_rate": 1,
			"party_type": 'Employee',
			"party": self.employee,
			"reference_type": self.doctype,
			"reference_name": self.name,
		})


		journal_entry.save(ignore_permissions=True)
		journal_entry.submit()

		lnk = get_link_to_form(journal_entry.doctype, journal_entry.name)
		frappe.msgprint(_("{} {} was Created").format(
			journal_entry.doctype, lnk))

	@frappe.whitelist()
	def get_total_ticket_amount(self):
		self.total_tickets = self.total_tickets or 0
		self.ticket_rate = get_employee_ticket_rate(self.employee , self.usage_date) or 0
		self.total_amount = self.ticket_rate * self.total_tickets


@frappe.whitelist()
def get_employee_ticket_rate(employee, on_date):
	ticket_rate = 0
	current_tickets = 0
	sql = f"""
		select 
			IFNULL(sum(total_amount),0) as total_amount,
			IFNULL(sum(total_tickets),0) as total_tickets
		from `tabEmployee Tickets` 
		where docstatus  = 1 and employee = '{employee}'
		and date('{on_date}') BETWEEN date(start_date) and date(end_date)
	"""
	res = frappe.db.sql(sql,as_dict=1) or 0
	if res:
		res = res[0]
		ticket_rate = ((res.total_amount or 0) / (res.total_tickets or 0)) if res.total_tickets else 0

	return ticket_rate , current_tickets
