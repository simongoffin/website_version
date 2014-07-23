# -*- coding: utf-8 -*-

from openerp.osv import osv


class view_version(osv.osv):
    _inherit = "ir.ui.view"
    
    def write(self, cr, user, ids, vals, context=None):
        #import pudb; pudb.set_trace()
        for view in self.browse(cr, user, ids, context=context):
            if 'arch' in vals and view.type == 'qweb':
                self.pool.get('website_version.old').create(cr, user, {
                    'view_id': view.id,
                    'arch': view.arch
                }, context=context)
        super(view_version, self).write(cr, user, ids, vals, context=None)
        
