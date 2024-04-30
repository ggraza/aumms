# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class RawMaterialBundle(Document):
	def autoname(self):
		for raw_material_details in self.get("raw_material_details"):
			raw_material_details.raw_material_id = f"{raw_material_details.item_name}-{raw_material_details.item_type}-{raw_material_details.quantity}"


	def on_submit(self):
		self.create_raw_material_request()
		self.mark_as_raw_material_bundle_created(created = 1)

	def on_cancel(self):
		self.mark_as_raw_material_bundle_created(created = 0)

	def create_raw_material_request(self):
	    for raw_material in self.raw_material_details:
	        if raw_material.quantity > raw_material.available_quantity_in_stock:
	            raw_material_request_exists = frappe.db.exists('Raw Material Request', {
	                'manufacturing_request': self.manufacturing_request,
	                'item_name': raw_material.item_name
	            })

	            if not raw_material_request_exists:
	                new_raw_material_request = frappe.new_doc('Raw Material Request')
	                new_raw_material_request.raw_material_request_type = "Raw Material Request"
	                new_raw_material_request.raw_material_bundle = self.name
	                new_raw_material_request.manufacturing_request = self.manufacturing_request
	                new_raw_material_request.required_date = self.item_required_date
	                new_raw_material_request.required_quantity = raw_material.quantity - raw_material.available_quantity_in_stock
	                new_raw_material_request.bundle_id = raw_material.raw_material_id
	                new_raw_material_request.append('raw_material_details', {
	                    'item_name': raw_material.item_name,
	                    'item_type': raw_material.item_type,
	                    'quantity': raw_material.quantity,
	                    'available_quantity_in_stock': raw_material.available_quantity_in_stock,
	                })
	                new_raw_material_request.insert(ignore_permissions=True)
	                frappe.msgprint("Raw Material Request Created.", indicator="green", alert=True)
	        else:
	            manufacturing_request_doc = frappe.get_doc('Manufacturing Request', self.manufacturing_request)
	            if manufacturing_request_doc:
	                for stage in manufacturing_request_doc.manufacturing_stages:
	                    if stage.manufacturing_stage == self.manufacturing_stage:
	                        frappe.db.set_value('Manufacturing  Stage', stage.name, 'raw_material_available', True)
	                        break


	def mark_as_raw_material_bundle_created(self, created):
		if frappe.db.exists('Manufacturing Request', self.manufacturing_request):
			manufacturing_request = frappe.get_doc('Manufacturing Request', self.manufacturing_request)
			if manufacturing_request:
				updated = False
				for stage in manufacturing_request.manufacturing_stages:
					if stage.manufacturing_stage == self.manufacturing_stage:
						stage.raw_material_bundle_created = created
						frappe.db.set_value('Manufacturing  Stage', stage.name, 'raw_material_bundle_created', created)
						break
