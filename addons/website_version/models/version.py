# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class ViewVersion(osv.Model):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views",copy=True),
        'snapshot_id' : fields.many2one('website_version.snapshot',ondelete='cascade', string="Snapshot_id"),
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
            snapshot_id=request.session.get('snapshot_id')[0]
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=context)[0]
            
            #from pudb import set_trace; set_trace()
            
            snap_ids=[]
            no_snap_ids=[]
            for id in ids:
                for view in snapshot.view_ids:
                 if view.master_id == id:
                    snap_ids.append(view.id)
                else:
                    copy_id=self.copy(cr,uid,id,{})
                    super(ViewVersion, self).write(cr, uid, copy_id, {'master_id':id,'snapshot_id':snapshot_id}, context=context)
                    super(ViewVersion, self).write(cr, uid,[id], {'version_ids': [(4, copy_id)]}, context=context)
                    snap.write(cr, uid,[snapshot_id], {'view_ids': [(4, copy_id)]}, context=context)
                    snap_ids.append(copy_id)
            super(ViewVersion, self).write(cr, uid, snap_ids, vals, context=context)
            
        except:
            super(ViewVersion, self).write(cr, uid, ids, vals, context=context)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        #from pudb import set_trace; set_trace()
        try :
            snapshot_id=request.session.get('snapshot_id')[0]
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=context)[0]
            print 'SNAPSHOT NAME={}'.format(snapshot.name)
            iuv = request.registry['ir.ui.view']
            iuv.clear_cache()

            #snap_views={}
            snap_ids=[]
            snap_trad={}
            all_views=self.browse(cr, uid, ids, context=context)
            for id in ids:
                for view in snapshot.view_ids:
                    if view.master_id == id:
                        current=self.browse(cr, uid, [id], context=context)[0]
                        snap_trad[view.id]=[current.id,current.xml_id,current.mode]
                        snap_ids.append(view.id)
                    else:
                        current=self.browse(cr, uid, [id], context=context)[0]
                        snap_trad[id]=[current.id,current.xml_id,current.mode]
                        snap_ids.append(id)
                    
            all_needed_views= super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
            all_needed_views_snapshot= super(ViewVersion, self).read(cr, uid, snap_ids, fields=fields, context=context, load=load)
            for view in all_needed_views_snapshot:
                view['id']=snap_trad[view['id']][0]
                view['xml_id']=snap_trad[view['id']][1]
                view['mode']=snap_trad[view['id']][2]
            return all_needed_views
        except:
            return super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
