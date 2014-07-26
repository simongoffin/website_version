(function () {
    'use strict';
    
    var website = openerp.website;

    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.website_version = {};

    instance.website_version.action = instance.web.Widget.extend({
        template: "website_version_templates",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var widget = new instance.website_version.ConfirmWidget(this);
            this.$("data-view-xmlid")
            $("button").click(function() {
                console.log("someone clicked on the button");
                
                openerp.jsonRpc( '/request_rpc', 'call', 
                {'xml_id': '1'})
                .then(function (result) {
                    console.log(result);
                })
                
            
            });
                
            },
    });
    
    website.ready().done(function() {
        var ace = new website_version.Ace();
        widget.appendTo(ace);
        
    });

})();