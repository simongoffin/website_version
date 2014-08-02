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
                //var id_seq=$("main").html();
                openerp.jsonRpc( '/all_snapshots', 'call', 
                {})
                
                .then(function (result) {
                    console.log(result);
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
                id: "editor_new_snapshot",
                window_title: _t("New snapshot"),
                input: "Snapshot name",
            }).then(function (name) {
            
                
                console.log(name);
                var context = website.get_context();
//                 website.session.model('website_version.snapshot')
//                             .call('create', ['', [['public','=','public']]], { context: website.get_context() });
                openerp.jsonRpc( '/create_snapshot', 'call', 
                {
                    'name':name,
                })
                .then(function (result) {
                    console.log('Snapshot '+name+' saved');
                    location.reload();
                })
                
                
            });
        },
        
        link_version: function() {
            var text = $(event.target).text();
            console.log('Youp clicked on ' + text);
            //var id_seq=$("main").html();
            openerp.jsonRpc( '/change_snapshot', 'call', 
                {
                    'snapshot_name':text,
                })
                .then(function (result) {
                    console.log(result);
                    location.reload();
                })
        },
    });
    
    website.ready().done(function() {
        console.log("This is the menu_version!");
    });
    
})();
