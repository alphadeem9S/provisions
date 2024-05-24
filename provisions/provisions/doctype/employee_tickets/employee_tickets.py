# Copyright (c) 2023, Peter Maged and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import getdate , formatdate

class EmployeeTickets(Document):

	def validate (self):
		self.set_totals()
		self.validate_dates()
		self.validate_overlap()

	def validate_dates(self):
		if getdate(self.start_date) > getdate(self.end_date):
			frappe.throw(_("End date can not be less than start date"))

	def validate_overlap(self):
		query = """
			select name
			from `tab{0}`
			where name != %(name)s
			and employee = %(employee)s
			and docstatus < 2
	and (start_date between %(start_date)s and %(end_date)s \
				or end_date between %(start_date)s and %(end_date)s \
				or (start_date < %(start_date)s and end_date > %(end_date)s))
			"""
		if not self.name:
			# hack! if name is null, it could cause problems with !=
			self.name = "New " + self.doctype

		overlap_doc = frappe.db.sql(
			query.format(self.doctype),
			{
				"start_date": self.start_date,
				"end_date": self.end_date,
				"name": self.name,
				"employee": self.employee
			},
			as_dict=1,
		)

		if overlap_doc:
			msg = (
				_("A {0} exists between {1} and {2} (").format(
					self.doctype, formatdate(
						self.start_date), formatdate(self.end_date)
				)
				+ """ <b><a href="/app/Form/{0}/{1}">{1}</a></b>""".format(
					self.doctype, overlap_doc[0].name)
				+ _(") for {0}").format(self.employee)
			)
			frappe.throw(msg)

	@frappe.whitelist()
	def set_totals(self):
		total_tickets  = 0
		total_amount  = 0
		for row in self.tickets :
			row.rate = row.rate or 0
			row.qty = row.qty or 0
			row.amount = row.qty * row.rate
			total_amount += row.amount
			total_tickets += row.qty
		self.total_amount = total_amount
		self.total_tickets = total_tickets

