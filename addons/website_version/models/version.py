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
#         for view in self.browse(cr, uid, ids, context=context):
#             if view.type == 'qweb' and 'arch' in vals and not 'inherit_id' in vals:
#                 copy_id=self.copy(cr,uid,view.id,{})
#                 #self.write(cr, uid, [copy_id], {'master_id':copy_id})
#                 super(ViewVersion, self).write(cr, uid,[copy_id], {'version_ids': [(4, view.id)]}, context=context)
#                 vals['master_id'] = copy_id
        try:
            iter(ids)
        except:
            ids=[ids]

        try:
            id_version=request.session.get('id_version')
            id_master=request.session.get('id_master')
            #from pudb import set_trace; set_trace()
            new_ids=[]
            
            for id in ids:
                if id==id_master:
                    new_ids.append(id_version)
                else:
                    new_ids.append(id)
            super(ViewVersion, self).write(cr, uid, new_ids, vals, context=context)
        except:
            super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def write_simple(self, cr, uid, ids, vals, context=None):
        super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        #from pudb import set_trace; set_trace()
        try :
            id_version=request.session.get('id_version')
            print 'ID VERSION={}'.format(id_version)
            #from pudb import set_trace; set_trace()
            id_master=request.session.get('id_master')
            iuv = request.registry['ir.ui.view']
            iuv.clear_cache()
            
        except:
            id_version= 287
            id_master=287
        if id_version==None or id_master==None:
            id_version= 287
            id_master=287
        version_arch=super(ViewVersion, self).read(cr, uid, [id_version], fields=['arch'], context=context, load=load)[0].get('arch')

        all_needed_views= super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        for view in all_needed_views:
            if view.get('id')==id_master:
                view['arch']=version_arch
                print 'LU'
        return all_needed_views
