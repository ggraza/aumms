# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class RawMaterialRequest(Document):

    @frappe.whitelist()
    def create_manufacturing_request(self):
        manufacturing_request_exists = frappe.db.exists('Manufacturing Request', {'raw_material_request': self.name})
        for item in self.raw_material_details:
            if not manufacturing_request_exists:
                manufacturing_request = frappe.new_doc('Manufacturing Request')
                manufacturing_request.request_from = 'Raw Material Request'
                manufacturing_request.raw_material_request = self.name
                manufacturing_request.jewellery_order = self.jewellery_order
                manufacturing_request.required_date = self.required_date
                manufacturing_request.quantity = self.required_quantity
                manufacturing_request.expected_weight = item.required_weight
                manufacturing_request.purity = self.purity
                manufacturing_request.weight =  item.required_weight
                manufacturing_request.supervisor_warehouse = self.supervisor_warehouse
                manufacturing_request.uom = self.uom
                manufacturing_request.type = self.item_type
                manufacturing_request.insert(ignore_permissions=True)
                frappe.msgprint(f"Manufacturing Request {manufacturing_request.name} created.", indicator="green", alert=1)
            else:
                frappe.throw(_('Manufacturing Request already exist for this {0}'.format(self.name)))

    @frappe.whitelist()
    def create_purchase_order(self):
        purchase_order = frappe.new_doc('Purchase Order')
        purchase_order.supplier = self.supplier
        for item in self.raw_material_details:
            purchase_order.append('items', {
                'item_code': item.item,
                'item_name': item.item,
                'schedule_date': self.required_date,
                'uom' : self.uom,
                'qty' :self.required_quantity,

            })
        purchase_order.insert(ignore_permissions=True)
        frappe.msgprint(f"Purchase Order created.", indicator="green", alert=1)
