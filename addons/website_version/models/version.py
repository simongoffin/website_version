# -*- coding: utf-8 -*-

from openerp.osv import osv,fields


class view_version(osv.osv):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views"),
    }
    
    def write(self, cr, user, ids, vals, context=None):
        import pudb; pudb.set_trace()
        for view in self.browse(cr, user, ids, context=context):
            if 'arch' in vals and view.type == 'qweb':
                old_view=self.read(cr, user, ids,['name','model','priority','type','arch',
                'inherit_id','inherit_children_ids','field_parent','model_data_id','xml_id',
                'groups_id','model_ids','create_date','write_date','mode','application'], context=None)
                #old_view['version_ids']=view
                #la nouvelle vue pointe vers son parent
                #vals['master_id']=
                self.create(cr, user, old_view, context=context)
        super(view_version, self).write(cr, user, ids, vals, context=None)
        
        
