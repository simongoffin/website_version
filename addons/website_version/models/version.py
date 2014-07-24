# -*- coding: utf-8 -*-
from openerp.osv import osv,fields


class view_version(osv.osv):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views"),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        from pudb import set_trace; set_trace()
        for view in self.browse(cr, uid, ids, context=context):
            if view.type == 'qweb' and vals.get('arch'):
                old_id=self.copy(cr,uid,view.id,{})
                super(view_version, self).write(cr, uid,[old_id], dict(version_ids=view), context=context)
                vals['master_id'] = old_id
        super(view_version, self).write(cr, uid, ids, vals, context=context)
