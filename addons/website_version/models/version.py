# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class ViewVersion(osv.Model):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views",copy=True),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        #from pudb import set_trace; set_trace()
        for view in self.browse(cr, uid, ids, context=context):
            if view.type == 'qweb' and 'arch' in vals and not 'inherit_id' in vals:
                copy_id=self.copy(cr,uid,view.id,{})
                #self.write(cr, uid, [copy_id], {'master_id':copy_id})
                super(ViewVersion, self).write(cr, uid,[copy_id], {'version_ids': [(4, view.id)]}, context=context)
                vals['master_id'] = copy_id
                
        super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def write_simple(self, cr, uid, ids, vals, context=None):
        super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        #from pudb import set_trace; set_trace()
        id_version= 287
        id_master=287
        version_arch=super(ViewVersion, self).read(cr, uid, [id_version], fields=['arch'], context=context, load=load)[0].get('arch')

#         xx=super(ViewVersion, self).read(cr, uid, [id_version], fields=fields, context=context, load=load)
#         yy=super(ViewVersion, self).read(cr, uid, [id_master], fields=fields, context=context, load=load)
        
#         version = self.poll['fsqdfsdf']
#         date_create = ....
#         new_ids = []
#         for id in ids:
#             if id==id_master:
#                 new_ids.append(id_version)
#             else:
#                 new_ids.append(id)
        all_needed_views= super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        for view in all_needed_views:
            if view.get('id')==id_master and 'arch' in view:
                view['arch']=version_arch
        return all_needed_views
