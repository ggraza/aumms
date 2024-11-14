frappe.listview_settings["AuMMS Item"] = {
  refresh: function (listview) {
    listview.page.add_actions_menu_item(
      __("Create Opening Stock"),
      function () {
        let docnames = listview.get_checked_items(true);
        frappe.call({
          method:
            "aumms.aumms.doctype.aumms_item.aumms_item.create_opening_stock_from_list",
          args: {
            item_list_json: JSON.stringify(docnames), // Convert list to JSON string
          },
          callback: function (r) {
            if (r.message) {
              console.log(r.message);
            }
          },
        });
      }
    );
  },
};
