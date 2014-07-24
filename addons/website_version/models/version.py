# -*- coding: utf-8 -*-

from openerp.osv import osv,fields


class view_version(osv.osv):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views"),
    }
    
    def write(self, cr, user, ids, vals, context=None):
        #import pudb; pudb.set_trace()
        for view in self.browse(cr, user, ids, context=context):
            if 'arch' in vals and view.type == 'qweb':
                old_view=self.read(cr, user, ids,['name','model','priority','type','arch',
                'field_parent','xml_id',
                'create_date','write_date','mode','application'], context=None)
                old_view['version_ids']=view
                old_id=self.create(cr, user, old_view, context=context)
                vals['master_id']=old_id
        super(view_version, self).write(cr, user, ids, vals, context=None)
