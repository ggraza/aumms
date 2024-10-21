import frappe
from frappe import _


def get_balance_qty(aumms_item_doc):
	filters = {
		"item_type": aumms_item_doc.item_type,
		"purity": aumms_item_doc.purity,
		"stock_uom": aumms_item_doc.weight_uom,
		"is_cancelled": 0,
	}
	return frappe.db.get_value("Metal Ledger Entry", filters, "balance_qty") or 0


def insert_metal_ledger_entry(
	doc, item, aumms_item_doc, balance_qty, is_reversal=False
):
	fields = {
		"doctype": "Metal Ledger Entry",
		"posting_date": doc.posting_date,
		"posting_time": doc.posting_time,
		"voucher_type": doc.doctype,
		"voucher_no": doc.name,
		"company": frappe.defaults.get_defaults().company,
		"item_code": item.item_code,
		"item_name": item.item_name,
		"stock_uom": aumms_item_doc.weight_uom,
		"purity": aumms_item_doc.purity,
		"purity_percentage": aumms_item_doc.purity_percentage,
		"board_rate": item.valuation_rate,
		"batch_no": item.batch_no,
		"item_type": aumms_item_doc.item_type,
		"balance_qty": balance_qty
		+ (
			aumms_item_doc.gold_weight
			if not is_reversal
			else -aumms_item_doc.gold_weight
		),
		"amount": item.amount if not is_reversal else -item.amount,
		"incoming_rate" if not is_reversal else "outgoing_rate": item.valuation_rate,
	}

	frappe.get_doc(fields).insert(ignore_permissions=1)


def process_metal_ledger(doc, is_reversal=False):
	if not doc.custom_keep_metal_ledger:
		return

	ledger_created = False
	for item in doc.items:
		aumms_item_doc = frappe.get_doc("AuMMS Item", item.item_code)
		balance_qty = get_balance_qty(aumms_item_doc)

		insert_metal_ledger_entry(doc, item, aumms_item_doc, balance_qty, is_reversal)
		ledger_created = True

	if ledger_created:
		action = _("reversed") if is_reversal else _("created")
		frappe.msgprint(
			_("Metal Ledger Entry is {0}.").format(action),
			indicator="green" if not is_reversal else "red",
			alert=1,
		)


def create_mle_against_sr(doc, method=None):
	"""
	Method to create metal ledger entries on submit.
	"""
	process_metal_ledger(doc)


def reverse_mle_against_sr(doc, method=None):
	"""
	Method to reverse metal ledger entries on cancel.
	"""
	process_metal_ledger(doc, is_reversal=True)
