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
        try:
            iter(ids)
        except:
            ids=[ids]

        try:
            snapshot_id=request.session['snapshot_id']
            if snapshot_id==0:
                raise 
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=context)[0]
            snap_ids=[]
            no_snap_ids=[]
            for id in ids:
                check=True
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        snap_ids.append(view.id)
                        check=False
                if check:
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
            iuv = request.registry['ir.ui.view']
            iuv.clear_cache()
            snapshot_id=request.session['snapshot_id']
            if snapshot_id==0:
                raise 
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=context)[0]
            #print 'SNAPSHOT NAME={}'.format(snapshot.name)
            snap_ids=[]
            snap_trad={}
            for id in ids:
                check=True
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        current=self.browse(cr, uid, [id], context=context)[0]
                        snap_trad[view.id]=[current.id,current.xml_id,current.mode]
                        snap_ids.append(view.id)
                        check=False
                if check:
                    snap_ids.append(id)
            all_needed_views_snapshot= super(ViewVersion, self).read(cr, uid, snap_ids, fields=fields, context=context, load=load)
            for view in all_needed_views_snapshot:
                if view['id'] in snap_trad:
                    view['mode']=snap_trad[view['id']][2]
                    view['xml_id']=snap_trad[view['id']][1]
                    view['id']=snap_trad[view['id']][0]
            return all_needed_views_snapshot
        except:
            return super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
