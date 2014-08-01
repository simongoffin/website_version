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
            snap_id=request.session.get('snapshot_id')
            snap = request.registry['website_version.snapshot']
            snap_date=snap.browse(cr, uid, snap_id, context=context)[0].create_date
            
            #from pudb import set_trace; set_trace()
            
            vals['create_date']=snap_date
            snap_ids=[]
            no_snap_ids=[]
            for view in self.browse(cr, uid, ids, context=context):
                 if view.create_date == snap_date:
                    snap_ids.append(view.id)
                else:
                    copy_id=self.copy(cr,uid,view.id,{})
                    super(ViewVersion, self).write(cr, uid, copy_id, {'master_id':view.id}, context=context)
                    super(ViewVersion, self).write(cr, uid,[view.id], {'version_ids': [(4, copy_id)]}, context=context)
                    snap_ids.append(copy_id)
            super(ViewVersion, self).write(cr, uid, snap_ids, vals, context=context)
            
        except:
            super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        #from pudb import set_trace; set_trace()
         try :
             snap_id=request.session.get('snapshot_id')
             snap = request.registry['website_version.snapshot']
             snap_date=snap.browse(cr, uid, snap_id, context=context)[0].create_date
             print 'SNAPSHOT NAME={}'.format(snap.name)
#             from pudb import set_trace; set_trace()
             iuv = request.registry['ir.ui.view']
             iuv.clear_cache()

#         version_arch=super(ViewVersion, self).read(cr, uid, [id_version], fields=['arch'], context=context, load=load)[0].get('arch')
# 
            all_needed_views= super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
            for view in all_needed_views:
                if view.get('id')==id_master:
                    view['arch']=version_arch
                    print 'LU'
        return super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
