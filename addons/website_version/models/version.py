# -*- coding: utf-8 -*-
from openerp.osv import osv,fields


class view_version(osv.osv):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views"),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        for view in self.browse(cr, uid, ids, context=context):
            if view.type == 'qweb' and vals.get('arch'):
                old_view_vals = view.read([
                    'name',
                    'model',
                    'priority',
                    'type',
                    'arch',
                    'field_parent',
                    'xml_id',
                    'create_date',
                    'write_date',
                    'mode',
                    'application'
                ])[0]
                old_view_vals['version_ids'] = view
                old_id = self.create(cr, uid, old_view_vals, context=context)
                vals['master_id'] = old_id
        super(view_version, self).write(cr, uid, ids, vals, context=context)
