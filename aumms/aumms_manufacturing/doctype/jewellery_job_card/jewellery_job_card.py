# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class JewelleryJobCard(Document):
    def before_insert(self):
        self.update_item_table()

    def on_submit(self):
        self.mark_as_completed(completed=1)
        self.create_metal_ledger()
        self.create_stock_ledger()
        self.update_product()
        self.create_item()

    def on_cancel(self):
        self.mark_as_completed(completed=0)

    def update_item_table(self):
        if frappe.db.exists('Raw Material Bundle', {'manufacturing_request': self.manufacturing_request}):
            raw_material_doc = frappe.get_doc('Raw Material Bundle', {'manufacturing_request': self.manufacturing_request})
            for item in raw_material_doc.items:
                self.append('item_details', {
                    'item': item.item,
                    'quantity': item.required_quantity,
                    'weight':item.required_weight
                })

    def mark_as_completed(self, completed):
        if frappe.db.exists('Manufacturing Request', self.manufacturing_request):
            manufacturing_request = frappe.get_doc('Manufacturing Request', self.manufacturing_request)
            if manufacturing_request:
                updated = False
                for stage in manufacturing_request.manufacturing_stages:
                    if stage.manufacturing_stage == self.stage:
                        stage.completed = completed
                        frappe.db.set_value('Manufacturing  Stage', stage.name, 'completed', completed)
                        manufacturing_request.mark_as_finished()
                        break

    def update_product(self):
        if frappe.db.exists('Manufacturing Request', self.manufacturing_request):
            manufacturing_request = frappe.get_doc('Manufacturing Request', self.manufacturing_request)
            if manufacturing_request:
                updated = False
                for stage in manufacturing_request.manufacturing_stages:
                    if stage.manufacturing_stage == self.stage:
                        for item in self.item_details:
                            frappe.db.set_value('Manufacturing  Stage', self.manufacturing_request, 'product', item.item)
                            frappe.db.set_value('Manufacturing  Stage', stage.name, 'weight', self.product_weight)
                            frappe.db.set_value('Manufacturing Request', self.manufacturing_request, 'weight', self.product_weight)
                            break

    def create_metal_ledger(self) :
        if self.keep_metal_ledger:
            for item in self.item_details:
                new_metal_ledger = frappe.new_doc('Metal Ledger Entry')
                new_metal_ledger.posting_date = frappe.utils.today()
                new_metal_ledger.posting_time = frappe.utils.now()
                new_metal_ledger.voucher_type = self.doctype
                new_metal_ledger.voucher_no = self.name
                new_metal_ledger.item_code = item.item
                new_metal_ledger.item_name = item.item
                new_metal_ledger.stock_uom = self.uom
                new_metal_ledger.item_type = self.type
                new_metal_ledger.purity = self.purity
                new_metal_ledger.out_qty = item.quantity
                new_metal_ledger.balance_qty = 0
                new_metal_ledger.insert(ignore_permissions = True)
                frappe.msgprint("Metal Ledger Created.", indicator="green", alert=1)

    def create_stock_ledger(self):
        if self.keep_metal_ledger:
            for item in self.item_details:
                new_stock_ledger = frappe.new_doc('Stock Ledger Entry')
                new_stock_ledger.posting_date = frappe.utils.today()
                new_stock_ledger.posting_time = frappe.utils.now()
                new_stock_ledger.voucher_type = self.doctype
                new_stock_ledger.voucher_no = self.name
                new_stock_ledger.item_code = item.item
                new_stock_ledger.stock_uom = self.uom
                new_stock_ledger.warehouse = self.smith_warehouse
                new_stock_ledger.purity = self.purity
                new_stock_ledger.actual_qty = item.quantity
                new_stock_ledger.balance_qty = 0
                new_stock_ledger.insert(ignore_permissions = True)
                frappe.msgprint("Stock Ledger Created.", indicator="green", alert=1)

    def create_item(self):
        warehouse = frappe.db.get_single_value('AuMMS Settings', 'item_group')
        if self.is_first_stage:
            new_item = frappe.new_doc('AuMMS Item')
            new_item.item_name = f"{self.purity} {self.type} {self.category} {self.expected_weight} {self.stage}"
            new_item.item_type = self.type
            new_item.item_group = warehouse
            new_item.stock_uom = self.uom
            new_item.item_category = self.category
            new_item.purity = self.purity
            new_item.gold_weight = self.expected_weight
            new_item.is_stock_item = True
            new_item.item_code = f"{self.purity} {self.type} {self.category} {self.stage} {self.expected_weight}"
            frappe.db.set_value('Jewellery Job Card', self.name, 'product', new_item.item_name)
            frappe.db.set_value('Manufacturing Request', self.manufacturing_request, 'product', new_item.item_code)
            new_item.save(ignore_permissions=True)
            frappe.msgprint("Item Created.", indicator="green", alert=1)
