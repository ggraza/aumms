// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jewellery Job Card", {
  refresh: function(frm){
    create_custom_buttons(frm);
  }
});

let create_custom_buttons = function(frm){
  if (frm.doc.status == "Open") {
    frm.add_custom_button('Start', () => {
      frm.set_value("status", "Processing");
      updateStartTime(frm);
      frm.save();
      frm.page.set_primary_action(__("Pause"), () => {
        create_custom_buttons(frm);
      }, "btn-primary");
    }).addClass("btn-primary");
  } else if (frm.doc.status == "Processing") {
    frm.add_custom_button(__("Pause"), () => {
      frm.set_value("status", "Hold");
      updateEndTime(frm);
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");

    frm.add_custom_button(__("Done"), () => {
      frm.set_value("status", "Complete");
      updateEndTime(frm);
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");
  } else if (frm.doc.status == "Hold") {
    frm.add_custom_button('Start', () => {
      frm.set_value("status", "Processing");
      updateStartTime(frm);
      frm.save();
      create_custom_buttons(frm);
    }).addClass("btn-primary");
  }
}

function updateStartTime(frm) {
  const currentTime = frappe.datetime.now_datetime();
    let row = frappe.model.add_child(frm.doc, 'Job Time', 'job_time');
    row.start_time = currentTime;
    frm.refresh_field("job_time");
}

function updateEndTime(frm) {
  const currentTime = frappe.datetime.now_datetime();
  frm.doc.job_time.forEach(function(row) {
    if (row.start_time && !row.end_time) {
      frappe.model.set_value(row.doctype, row.name, 'end_time', currentTime);
    }
  });
}
