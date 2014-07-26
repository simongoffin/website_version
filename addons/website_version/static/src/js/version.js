(function () {
    'use strict';
    var website = openerp.website;
    website.add_template_file('/website_version/static/src/xml/previous_button.xml');
    website.EditorBar.include({
        start: function () {
            var self = this;
            console.log("Are you ready!");
            return this._super();
        },
    });
        
})();

