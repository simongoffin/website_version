# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class MenuVersion(osv.Model):
    _inherit = "website.menu"
    
    _columns = {
        'snapshot_name' : fields.char(string="Title", size=256),
    }
    
    _defaults = {
        'snapshot_name': 'Master',
    }
    
    def get_tree(self, cr, uid, website_id, context=None):
        def make_tree(node):
            menu_node = dict(
                id=node.id,
                name=node.name,
                url=node.url,
                new_window=node.new_window,
                sequence=node.sequence,
                parent_id=node.parent_id.id,
                children=[],
                snapshot_name=node.snapshot_name
            )
            for child in node.child_id:
                menu_node['children'].append(make_tree(child))
            return menu_node
        menu = self.pool.get('website').browse(cr, uid, website_id, context=context).menu_id
        return make_tree(menu)