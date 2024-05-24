# Copyright (c) 2023, Peter Maged and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.data import date_diff, flt, get_link_to_form
from dateutil import parser
from dateutil import relativedelta


class ProvisionEntry(Document):

    def validate(self):
        self.get_employee_details()
        self.set_totals()

    def on_submit(self):
        if not getattr(self, 'employees', []):
            frappe.throw(_("There is no valid employees from {} to {}").format(
                self.start_date, self.end_date))
        self.create_journal_entry()

    def create_journal_entry(self):
        if not frappe.db.exists("Provisions Settings", self.company):
            frappe.throw(
                _("Please Create Provisions Settings for Company {}").format(self.company))
        settings = frappe.get_doc("Provisions Settings", self.company)
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = "Journal Entry"
        journal_entry.user_remark = _("Provisions Journal Entry for employees from {0} to {1}").format(
            self.start_date, self.end_date
        )
        journal_entry.company = self.company
        journal_entry.posting_date = self.posting_date

        precision = frappe.get_precision(
            "Journal Entry Account", "debit_in_account_currency")
        credit_precision = frappe.get_precision(
            "Journal Entry Account", "credit_in_account_currency")
        

        # Salaries
        # total_salaries = sum([flt((x.salary or 0), precision)
        #                      for x in self.employees if x.employee_type != "Operation"])
        # operation_total_salaries = sum([flt((x.salary or 0), precision)
        #                      for x in self.employees if x.employee_type == "Operation"])

        # journal_entry.append('accounts', {
        #     "account": settings.end_of_service_expense_account,
        #     # self.total_salary,
        #     "debit_in_account_currency": flt(total_salaries, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.end_of_service_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })

        # journal_entry.append('accounts', {
        #     "account": settings.end_of_service_operation_expense_account,
        #     # self.total_salary,
        #     "debit_in_account_currency": flt(operation_total_salaries, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.end_of_service_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })
        # Tickets
        total_tickets = sum([flt((x.tickets or 0), precision)
                            for x in self.employees  if x.employee_type != "Operation"])
        total_operation_tickets = sum([flt((x.tickets or 0), precision)
                            for x in self.employees  if x.employee_type == "Operation"])

        # journal_entry.append('accounts', {
        #     "account": settings.tickets_expense_account,
        #     # self.total_tickets,
        #     "debit_in_account_currency": flt(total_tickets, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.tickets_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })

        # journal_entry.append('accounts', {
        #     "account": settings.tickets_operation_expense_account,
        #     # self.total_tickets,
        #     "debit_in_account_currency": flt(total_operation_tickets, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.tickets_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })

        # Leaves
        # total_leave = sum([flt((x.leaves or 0), precision)
        #                   for x in self.employees  if x.employee_type != "Operation"])
        # total_operation_leave = sum([flt((x.leaves or 0), precision)
        #                   for x in self.employees  if x.employee_type == "Operation"])

        # journal_entry.append('accounts', {
        #     "account": settings.leaves_expense_account,
        #     # self.total_leave,
        #     "debit_in_account_currency": flt(total_leave, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.leaves_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })

        # journal_entry.append('accounts', {
        #     "account": settings.leaves_operation_expense_account,
        #     # self.total_leave,
        #     "debit_in_account_currency": flt(total_operation_leave, precision),
        #     "exchange_rate": 1,
        #     # "cost_center": self.cost_center or settings.leaves_expense_cost_center,
        #     # "project": self.project,
        #     "reference_type": self.doctype,
        #     "reference_name": self.name,

        # })

        for row in self.employees:
            
            project , cost_center ,employee_type = frappe.db.get_value("Employee" , row.employee , [
                'project' ,
                'cost_center' ,
                'employee_type'
            ])

            # Salaries
            if row.salary :
                journal_entry.append('accounts', {
                    "account": settings.end_of_service_provision_account,
                    "credit_in_account_currency": flt(row.salary, credit_precision),
                    "exchange_rate": 1,
                    "party_type": 'Employee',
                    "party": row.employee,
                    "reference_type": self.doctype,
                    "reference_name": self.name,

                })

                journal_entry.append('accounts', {
                    "account": settings.end_of_service_operation_expense_account if employee_type == "Operation" else settings.end_of_service_expense_account,
                    # self.total_salary,
                    "debit_in_account_currency": flt(row.salary, precision),
                    "exchange_rate": 1,
                    "cost_center": cost_center or  self.cost_center or settings.end_of_service_cost_center,
                    "project": project or self.project,
                    # "cost_center": self.cost_center or settings.end_of_service_expense_cost_center,
                    # "project": self.project,
                    "reference_type": self.doctype,
                    "reference_name": self.name,

                })



            # Tickets
            if row.tickets :
                journal_entry.append('accounts', {
                    "account": settings.tickets_provision_account,
                    "credit_in_account_currency": flt(row.tickets, credit_precision),
                    "exchange_rate": 1,
                    # "cost_center": cost_center or self.cost_center or settings.tickets_cost_center,
                    # "project": project or self.project,
                    "party_type": 'Employee',
                    "party": row.employee,
                    "reference_type": self.doctype,
                    "reference_name": self.name,
                })

                journal_entry.append('accounts', {
                    "account": settings.tickets_operation_expense_account if employee_type == "Operation" else settings.tickets_expense_account,
                    # self.total_salary,
                    "debit_in_account_currency": flt(row.tickets, precision),
                    "exchange_rate": 1,
                    "cost_center": cost_center or  self.cost_center or settings.tickets_cost_center,
                    "project": project or self.project,
                    # "cost_center": self.cost_center or settings.end_of_service_expense_cost_center,
                    # "project": self.project,
                    "reference_type": self.doctype,
                    "reference_name": self.name,

                })

            # Leaves
            # Tickets
            if row.leaves :
                journal_entry.append('accounts', {
                    "account": settings.leaves_provision_account,
                    "credit_in_account_currency": flt(row.leaves, credit_precision),
                    "exchange_rate": 1,
                    # "cost_center":  cost_center or self.cost_center or settings.leaves_cost_center,
                    # "project": project or self.project,
                    "party_type": 'Employee',
                    "party": row.employee,
                    "reference_type": self.doctype,
                    "reference_name": self.name,

                })

                journal_entry.append('accounts', {
                    "account": settings.leaves_operation_expense_account if employee_type == "Operation" else settings.leaves_expense_account,
                    # self.total_salary,
                    "debit_in_account_currency": flt(row.leaves, precision),
                    "exchange_rate": 1,
                    # "cost_center": self.cost_center or settings.end_of_service_expense_cost_center,
                    # "project": self.project,
                    "cost_center": cost_center or  self.cost_center or settings.leaves_cost_center,
                    "project": project or self.project,
                    "reference_type": self.doctype,
                    "reference_name": self.name,

                })
        journal_entry.save(ignore_permissions=True)

        lnk = get_link_to_form(journal_entry.doctype, journal_entry.name)
        frappe.msgprint(_("{} {} was Created").format(
            journal_entry.doctype, lnk))

    @frappe.whitelist()
    def set_totals(self):
        self.total_employees = 0
        self.total_salary = 0
        self.total_leave = 0
        self.total_tickets = 0

        for row in self.employees:
            row.salary = row.salary or 0
            row.tickets = row.tickets or 0
            row.leaves = row.leaves or 0

            self.total_employees += 1
            self.total_salary += row.salary
            self.total_leave += row.leaves
            self.total_tickets += row.tickets

    @frappe.whitelist()
    def get_employee_details(self):
        employees = self.get_employees()
        self.set('employees', [])
        for emp in employees:
            joining_date, relieving_date = emp.joining_date, emp.relieving_date
            if joining_date:
                joining_date = parser.parse(str(joining_date)).date()
            if relieving_date:
                relieving_date = parser.parse(str(relieving_date)).date()
            self.start_date = parser.parse(str(self.start_date)).date()
            self.end_date = parser.parse(str(self.end_date)).date()
            salary = get_employee_salary(
                emp.name, self.start_date, self.end_date, joining_date, relieving_date) or 0
            tickets = get_employee_tickets(
                emp.name, self.start_date, self.end_date, joining_date, relieving_date) or 0
            leaves = get_employee_leaves(
                emp.name, self.start_date, self.end_date, joining_date, relieving_date) or 0
            if salary or tickets or leaves:
                self.append('employees', {
                    "employee": emp.name,
                    "employee_name": emp.employee_name,
                    "employee_type":emp.employee_type,
                    "department": emp.department,
                    'salary': salary,
                    'tickets': tickets,
                    'leaves': leaves,
                })
        self.set_totals()

    def get_employees(self):
        conditions = self.get_employee_filters()
        sql = f"""
			select
				emp.name , emp.employee_name , emp.department , emp.date_of_joining as joining_date, emp.relieving_date, emp.employee_type
			from `tabEmployee` emp
			where emp.name not in
			(
				select detail.employee from `tabProvisions Employee` detail inner join `tab{self.doctype}` doc on doc.name = detail.parent
				where doc.docstatus < 2 and doc.payroll_period = '{self.payroll_period}' and doc.name <> '{self.name}'
			)
			{conditions}
		"""

        return frappe.db.sql(sql, as_dict=1)

    def get_employee_filters(self):
        conditions = f" and emp.status = 'Active' "

        data = getattr(self, 'company', None)
        if data:
            conditions += f" and emp.company = '{data}' "

        data = getattr(self, 'department', None)
        if data:
            conditions += f" and emp.department = '{data}' "

        data = getattr(self, 'designation', None)
        if data:
            conditions += f" and emp.designation = '{data}' "

        data = getattr(self, 'branch', None)
        if data:
            conditions += f" and emp.branch = '{data}' "

        data = getattr(self, 'employee', None)
        if data:
            conditions += f" and emp.name = '{data}' "

        return conditions


@frappe.whitelist()
def get_employee_salary(employee, start_date, end_date, joining_date, relieving_date):
    salary = 0
    sa_name = check_sal_struct(
        employee, start_date, end_date, joining_date, relieving_date)
    if sa_name:
        salary_structure_assignment = frappe.get_doc(
            "Salary Structure Assignment", sa_name)
        components = ['base', 'transportation_allowance', 'housing_allowance' , 'other_allowances']
        total = 0
        for i in components:
            total += getattr(salary_structure_assignment, i, 0)

        # frappe.msgprint(str(total))
        total = total / 24

        delta = relativedelta.relativedelta(start_date, joining_date)
        total_years = delta.years
        if total_years >= 5:
            total = total * 2
        salary = get_amount_on_payment_days(
            total, start_date, end_date, joining_date, relieving_date)

    return salary


@frappe.whitelist()
def get_employee_tickets(employee, start_date, end_date, joining_date, relieving_date):
    tickets = 0
    sql = f"""
		select
			IFNULL(sum(total_amount),0) as total_tickets
		from `tabEmployee Tickets`
		where docstatus  = 1 and employee = '{employee}'
		and (
			(date(start_date) BETWEEN date('{start_date}') and date('{end_date}'))
			or (date(end_date) BETWEEN date('{start_date}') and date('{end_date}'))
			or (date(start_date) <=  date('{start_date}') and date(end_date) >=  date('{end_date}'))
		)
	"""
    # frappe.msgprint(str(sql))
    total = frappe.db.sql(sql) or 0
    if total:
        total = total[0][0] or 0
    total = total / 12
    tickets = get_amount_on_payment_days(
        total, start_date, end_date, joining_date, relieving_date)
    return tickets


@frappe.whitelist()
def get_employee_leave_salary(employee, start_date, end_date, joining_date, relieving_date):
    total_salary = 0
    sa_name = check_sal_struct(
        employee, start_date, end_date, joining_date, relieving_date)
    if not sa_name:
        return 0
    salary_structure_assignment = frappe.get_doc(
        "Salary Structure Assignment", sa_name)
    components = ['base', 'transportation_allowance', 'housing_allowance' , 'other_allowances']
    # components = ['base']
    total_salary = 0
    for i in components:
        total_salary += getattr(salary_structure_assignment, i, 0)
    if not total_salary:
        return 0
    return total_salary


@frappe.whitelist()
def get_employee_leaves(employee, start_date, end_date, joining_date, relieving_date):
    leaves = 0

    total_salary = get_employee_leave_salary(employee, start_date, end_date,
                                             joining_date, relieving_date) or 0
    sql = f"""
		select 
			IFNULL(sum(total_leaves_allocated),0) as total_leaves
		from `tabLeave Allocation` 
		where docstatus  = 1 and employee = '{employee}'
		and (
			(date(from_date) BETWEEN date('{start_date}') and date('{end_date}'))
			or (date(to_date) BETWEEN date('{start_date}') and date('{end_date}'))
			or (date(from_date) <=  date('{start_date}') and date(to_date) >=  date('{end_date}'))
		)
	"""
    # frappe.msgprint(str(sql))
    total_leaves = frappe.db.sql(sql) or 0
    if total_leaves:
        total_leaves = total_leaves[0][0] or 0

    total = total_salary * total_leaves / 30

    total = total / 12
    leaves = get_amount_on_payment_days(
        total, start_date, end_date, joining_date, relieving_date)
    return leaves


def check_sal_struct(employee, start_date, end_date, joining_date, relieving_date):
    cond = """and sa.employee=%(employee)s and (sa.from_date <= %(start_date)s or
			sa.from_date <= %(end_date)s or sa.from_date <= %(joining_date)s)"""

    st_name = frappe.db.sql("""
		select sa.salary_structure , sa.name as salary_structure_assignment
		from `tabSalary Structure Assignment` sa join `tabSalary Structure` ss
		where sa.salary_structure=ss.name
			and sa.docstatus = 1 and ss.docstatus = 1 and ss.is_active ='Yes' %s
		order by sa.from_date desc
		limit 1
	""" % cond, {'employee': employee, 'start_date': start_date,
              'end_date': end_date, 'joining_date': joining_date}, as_dict=1)

    if st_name:
        salary_structure = st_name[0].salary_structure
        salary_structure_assignment = st_name[0].salary_structure_assignment
        return salary_structure_assignment

    else:
        frappe.msgprint(_("No active or default Salary Structure found for employee {0} for the given dates")
                        .format(employee), title=_('Salary Structure Missing'))


@frappe.whitelist()
def get_amount_on_payment_days(amount, start_date, end_date, joining_date, relieving_date):
    result = 0
    day_rate = amount / 30
    if joining_date:
        start_date = max(start_date, joining_date)
    if relieving_date:
        end_date = min(end_date, relieving_date)
    payment_days = min(date_diff(end_date, start_date) + 1, 30)
    payment_days = payment_days if payment_days > 0 else 0
    result = day_rate * payment_days
    # if payment_days < 30 :
    # 	result = day_rate * payment_days
    # else :
    # 	result = amount
    # frappe.msgprint(str(start_date))
    # frappe.msgprint(str(end_date))
    # frappe.msgprint(str(amount))
    # frappe.msgprint(str(day_rate))
    # frappe.msgprint(str(payment_days))
    # frappe.msgprint(str(result))

    return result or 0
