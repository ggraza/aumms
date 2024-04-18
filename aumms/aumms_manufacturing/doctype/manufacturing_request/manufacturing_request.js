// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Manufacturing Request", {
  refresh: function(frm) {
		frm.set_query('uom',()=>{
			return {
				filters: {
					"is_purity_uom": 1
				}
			}
		});
    frm.set_query('smith', 'manufacturing_stages', () =>{
      return{
        filters :{
          "designation" : "Smith"
        }
      }
    });
  }
});

frappe.ui.form.on("Manufacturing  Stage", {
  create_raw_material_bundle: function(frm, cdt , cdn) {
    let row = locals[cdt][cdn];
    frappe.new_doc('Raw Material Bundle', {
      'manufacturing_request': frm.doc.name,
      'manufacturing_stage' : row.manufacturing_stage,
    })
    row.raw_material_bundle_created = 1;
  },

  create_job_card: function(frm, cdt, cdn) {
    frm.call('create_jewellery_job_card', { 'stage_row_id': cdn }).then(r => {
      frm.refresh_fields();
    });
  },

  is_raw_material_from_previous_stage: function(frm, cdt, cdn) {
    let row = locals[cdt][cdn]
    if (row.is_raw_material_from_previous_stage) {
      frm.call('update_previous_stage', {idx:row.idx}).then(r=>{
        row.previous_stage = r.message
        frm.refresh_fields()
      })
    }
  },
  raw_material_available: function(frm, cdt, cdn) {
    let d = frm.doc.manufacturing_stages;
    let current_index = -1;
    for (let i = 0; i < d.length; i++) {
      if (d[i].name === cdn) {
        current_index = i;
        break;
      }
    }
    if (frm.doc.manufacturing_stages[current_index].raw_material_available) {
      if (current_index < d.length - 1) {
        let next_row = d[current_index + 1];
        next_row.allow_to_start_only_if_raw_material_available = 1;
        frm.refresh_field('manufacturing_stages');
      }
    }
  },
});
