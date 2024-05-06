// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Raw Material Bundle", {
  refresh: function(frm) {
    frm.set_query("item", "items", () => {
      return {
        filters: {
          "custom_is_raw_material": 1
        }
      };
    });
  },
  on_submit: function(frm) {
    if (!frm.doc.raw_material_available) {
      frm.add_custom_button('Create Raw Material Request', () => {
				frappe.call({
					method: 'aumms.aumms_manufacturing.doctype.raw_material_bundle.raw_material_bundle.create_raw_material_request',
					args: {
						docname: frm.doc.name
					},
					freeze: true,
					callback: (r) => {
						frm.reload_doc();
            var raw_material_request = r.message;
            if (raw_material_request) {
              frappe.set_route('Form', 'Raw Material Request', raw_material_request.name);
            }
					}
				});
			});
    }
  }
});
