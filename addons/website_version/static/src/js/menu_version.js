(function() {
    'use strict';
    var _t = openerp._t;
    
    var website=openerp.website;
    var QWeb = openerp.qweb;
    website.add_template_file('/website_version/static/src/xml/all_versions.xml');
    
    
    website.EditorBarContent.include({
        start: function() {
            $('#version-menu-button').click(function() {
                openerp.jsonRpc( '/all_snapshots', 'call', 
                {})
                
                .then(function (result) {
                    if($(".all_versions").length > 0){
                        $(".all_versions").html().replace(QWeb.render("all_versions", {mytab:result}));
                    }
                    else{
                        $( ".snapshot" ).append(QWeb.render("all_versions", {mytab:result}));
                    }
                 })                
            });
            return this._super();
        },
        
        snapshot: function() {
            website.prompt({
                id: "editor_new_snapshot",
                window_title: _t("New snapshot"),
                input: "Snapshot name",
            }).then(function (name) {               
                var context = website.get_context();
                openerp.jsonRpc( '/create_snapshot', 'call', 
                {
                    'name':name,
                })
                .then(function (result) {
                    location.reload();
                })                               
            });
        },
        
        change_snapshot: function() {
            var text = $(event.target).text();
            openerp.jsonRpc( '/change_snapshot', 'call', 
                {
                    'snapshot_name':text,
                })
                .then(function (result) {
                    location.reload();
                })
        },

        delete_snapshot: function() {
            var text = $(event.target).text();
            openerp.jsonRpc( '/delete_snapshot', 'call', 
                {})
                .then(function (result) {
                    location.reload();
                })
        },
    });
    
    website.ready().done(function() {
    });
    
})();
