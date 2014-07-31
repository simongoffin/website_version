(function() {
    'use strict';
    var _t = openerp._t;
    
    var website=openerp.website;
    var QWeb = openerp.qweb;
    website.add_template_file('/website_version/static/src/xml/all_versions.xml');
    
    
    website.EditorBarContent.include({
        start: function() {
            $('#version-menu-button').click(function() {
                console.log("Version clicked!");
                var id_seq=$("main").html();
                openerp.jsonRpc( '/all_versions', 'call', 
                {'id_seq' : id_seq})
                
                .then(function (result) {
                    if($(".all_versions").length > 0){
                        $(".all_versions").html().replace(QWeb.render("all_versions", {mytab:result}));
                    }
                    else{
                        $( ".snapshot" ).append(QWeb.render("all_versions", {mytab:result}));
                    }
                    console.log(result);
                })
                
            });
            return this._super();
        },
        
        snapshot: function() {
            console.log("Snapshot!");
            website.prompt({
                id: "editor_new_page",
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
        
        link_version: function() {
            var text = $(event.target).text();
            console.log('Youp clicked on '+parseInt(text));
            var id_seq=$("main").html();
            openerp.jsonRpc( '/change_version', 'call', 
                {
                    'id_seq' : id_seq ,
                    'id_version' : parseInt(text)
                })
                .then(function (result) {
                    location.reload();
                    console.log(result);
                })
        },
    });
    
    website.ready().done(function() {
        console.log("This is the menu_version!");
    });
    
})();
