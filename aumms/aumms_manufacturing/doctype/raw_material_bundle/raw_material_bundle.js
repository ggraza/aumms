// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Raw Material Bundle", {
	refresh : function(frm) {
    frm.set_query("item", "items", ()=> {
			return {
				filters: {
					"custom_is_raw_material" : 1
				}
			}
		});
	},
});
