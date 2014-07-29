(function() {
    'use strict';
    var _t = openerp._t;
    
    var website=openerp.website;
    //website.add_template_file('/website_version/static/src/xml/menu_version.xml');
    
    
        website.EditorBarContent.include({
        start: function() {
            return this._super();
        },
        
        snapshot: function() {
            console.log("Snapshot!");
            website.prompt({
                id: "editor_new_snapshot",
                window_title: _t("New snapshot"),
                input: _t("Page Title"),
                init: function () {
                    var $group = this.$dialog.find("div.form-group");
                    $group.removeClass("mb0");

                    var $add = $(
                        '<div class="form-group mb0">'+
                            '<label class="col-sm-offset-3 col-sm-9 text-left">'+
                            '    <input type="checkbox" checked="checked" required="required"/> '+
                            '</label>'+
                        '</div>');
                    $add.find('label').append(_t("Add page in menu"));
                    $group.after($add);
                }
            }).then(function (val, field, $dialog) {
                if (val) {
                    var url = '/website/add/' + encodeURIComponent(val);
                    if ($dialog.find('input[type="checkbox"]').is(':checked')) url +="?add_menu=1";
                    document.location = url;
                }
            });
        },
    });
    
    website.ready().done(function() {
        console.log("This is the menu_version!");
    });
    
})();
