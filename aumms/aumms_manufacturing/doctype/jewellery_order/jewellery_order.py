# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document


class JewelleryOrder(Document):

	def on_submit(self):
		# if self.quantity > self.quantity_of_available_item:
			self.create_manufacturing_request()

	def on_update(self):
		self.update_status()

	def update_status(self):
	    if frappe.db.exists('Customer Jewellery Order', {'name': self.customer_jewellery_order, 'status': 'Open'}):
	        customer_jewellery_order_status = frappe.get_doc('Customer Jewellery Order', {'name': self.customer_jewellery_order, 'status': 'Open'})
	        if customer_jewellery_order_status:
	            if customer_jewellery_order_status.status != self.status:
	                frappe.db.set_value('Customer Jewellery Order', self.customer_jewellery_order, 'status', self.status)

	def create_manufacturing_request(self):
		"""Create Manufacturing Request For Jewellery Order"""
		manufacturing_request_exists = frappe.db.exists('Manufacturing Request', {"jewellery_order": self.name})
		if not manufacturing_request_exists:
			for item in self.item_details:
				new_manufacturing_request = frappe.new_doc('Manufacturing Request')
				new_manufacturing_request.raw_material_request_type = "Jewellery Order"
				new_manufacturing_request.jewellery_order = self.name
				new_manufacturing_request.jewellery_order_design = self.design
				new_manufacturing_request.required_date = self.required_date
				new_manufacturing_request.item_name = item.item
				if self.expected_total_weight >=  self.total_weight:
					new_manufacturing_request.total_weight = self.expected_total_weight - self.total_weight
				else :
					new_manufacturing_request.total_weight = self.total_weight - self.expected_total_weight
				# new_manufacturing_request.uom = self.uom
				new_manufacturing_request.purity = self.purity
				new_manufacturing_request.type = self.type
				# if self.stock_available:
				# 	if self.quantity >= self.quantity_of_available_item:
				# 		total_quantity = self.quantity - self.quantity_of_available_item
				# 	else:
				# 		total_quantity = self.quantity_of_available_item - self.quantity
				# else:
				# 	total_quantity = self.quantity
				new_manufacturing_request.quantity = self.quantity
				new_manufacturing_request.category = self.category
				new_manufacturing_request.insert(ignore_permissions=True)
				item.requested_for_manufacturing = 1
				frappe.msgprint(f"Manufacturing Request {new_manufacturing_request.name} Created.", indicator="green", alert=1)
		else:
			frappe.throw(_('Manufacturing request for Jewellery Order {0} already exists'.format(self.name)))
