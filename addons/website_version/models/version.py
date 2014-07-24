# -*- coding: utf-8 -*-
from openerp.osv import osv,fields


class ViewVersion(osv.Model):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views",copy=True),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        #from pudb import set_trace; set_trace()
        for view in self.browse(cr, uid, ids, context=context):
            if view.type == 'qweb' and vals.get('arch'):
                old_id=self.copy(cr,uid,view.id,{})
                super(ViewVersion, self).write(cr, uid,[old_id], {'version_ids': [(4, old_id)]}, context=context)
                vals['master_id'] = old_id
        super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
