// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jewellery Job Card", {
  refresh: function(frm){
    create_custom_buttons(frm);
  },
});

let create_custom_buttons = function(frm){
  if (frm.doc.status == "Open") {
    frm.add_custom_button('Start', () => {
      frm.set_value("status", "Processing");
      frm.save();
      frm.page.set_primary_action(__("Pause"), () => {
        create_custom_buttons(frm);
      }, "btn-primary");
    }).addClass("btn-primary");
  } else if (frm.doc.status == "Processing") {
    frm.add_custom_button(__("Pause"), () => {
      frm.set_value("status", "Hold");
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");
  } else if (frm.doc.status == "Hold") {
    frm.add_custom_button('Start', () => {
      frm.set_value("status", "Processing");
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");

    frm.add_custom_button(__("Done"), () => {
      frm.set_value("status", "Complete");
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");
  }
}
