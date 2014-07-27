openerp.website_version = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.website_version = {};

    instance.website_version.action = instance.web.Widget.extend({
        template: "website.ace_view_editor",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            $("#my_button_preview").click(function() {
                console.log("You just clicked!");
                
                var id_seq=$("main").html();
                
                openerp.jsonRpc( '/request_rpc', 'call', 
                {'id_seq' : id_seq})
                .then(function (result) {
                    console.log(result);
                })
                
            });
            
                
            },
    });
    
};


