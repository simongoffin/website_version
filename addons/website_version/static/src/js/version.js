openerp.website_version = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.website_version = {};

    instance.website_version.action = instance.web.Widget.extend({
        template: "website.user_navbar",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            $("button").click(function() {
                console.log("someone clicked on the button");
                
                
                
            });
            
                
            },
    });
    
    $( document ).ready(function() {
    console.log( "ready!" );
    });
        
})();

