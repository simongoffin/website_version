(function() {
    'use strict';
    var hash = "#advanced-view-editor";
    var _t = openerp._t;
    
    var website=openerp.website;
    website.add_template_file('/website_version/static/src/xml/preview.xml');
    //website.add_template_file('/website_version/static/src/xml/version_menu.xml');

    website.action= {};

    website.action.Preview = openerp.Widget.extend({
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            console.log("This is another solution!");
            console.log($('.btn.btn-primary.btn-xs').get());
            $('.btn.btn-primary.btn-xs').click(function() {
                console.log("You just clicked!");
                
//                 var id_seq=$("main").html();
//                 
//                 openerp.jsonRpc( '/request_rpc', 'call', 
//                 {'id_seq' : id_seq})
//                 .then(function (result) {
//                     console.log(result);
//                 })
                
            });
            
                
            },
    });
    
    website.ace.ViewEditor.include({
        start: function() {
            console.log("This is my solution!!!");
            $('#my_button_preview').click(function() {
                console.log("You just clicked!");
                
                 var id_seq=$("main").html();
                openerp.jsonRpc( '/request_rpc', 'call', 
                {'id_seq' : id_seq})
                .then(function (result) {
                    //location.reload();
                    console.log(result);
                })
                
            });
            return this._super();
        },
    });
    
    website.ready().done(function() {
        console.log("This is the solution!");
        var preview=new website.action.Preview();
        preview.appendTo($('#oe_editzone'));
    });
    
})();


