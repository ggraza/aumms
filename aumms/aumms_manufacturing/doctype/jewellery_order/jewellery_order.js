// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jewellery Order", {
	refresh: function(frm) {
		if (!frm.is_new()){
			frm.set_df_property('customer_jewellery_order', 'read_only', 1)
			frm.set_df_property('customer', 'read_only', 1)
			frm.set_df_property('required_date', 'read_only', 1)
			frm.set_df_property('expected_total_weight', 'read_only', 1)
			// frm.set_df_property('customer_expected_amount', 'read_only', 1)
			frm.set_df_property('total_weight', 'read_only', 1)
			frm.set_df_property('quantity', 'read_only', 1)
			frm.set_df_property('design', 'read_only', 1)
		}
		frm.set_query('uom',()=>{
			return {
				filters: {
					"is_purity_uom": 1
				}
			}
		});
		frm.set_query("item", "item_details", ()=> {
			return {
				filters: {
					"item_type": frm.doc.type,
					"item_category": frm.doc.category
				}
			}
		});
  	},
		quantity_of_available_item: function(frm) {
			limit_item_details(frm)
		}

});

frappe.ui.form.on("Jewellery Order Items",{
  weight: function(frm, cdt, cdn){
   let d = locals[cdt][cdn];
   var total_weightage = 0
   frm.doc.item_details.forEach(function(d){
     total_weightage += d.weight;
   })
   frm.set_value('total_weight',total_weightage)
 },
 item_details_remove:function(frm){
     var total_weightage = 0
     frm.doc.item_details.forEach(function(d){
       total_weightage += d.weight;
     })
     frm.set_value("total_weight",total_weightage)
   },
   item_details_add: function(frm)  {
    limit_item_details(frm)
   }
});

function limit_item_details(frm) {
	if(frm.doc.quantity <= frm.doc.quantity_of_available_item){
		availa_quantity = frm.doc.quantity
	}
	else if(frm.doc.quantity >= frm.doc.quantity_of_available_item){
		availa_quantity = frm.doc.quantity_of_available_item
	}
  // limit = frm.doc.quantity - frm.doc.quantity_of_available_item
	limit = availa_quantity
  if (frm.doc.item_details.length >= limit)  {
    $(".btn.btn-xs.btn-secondary.grid-add-row").hide();
  }
  else  {
    $(".btn.btn-xs.btn-secondary.grid-add-row").show();
  }
}
