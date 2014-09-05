# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class ViewVersion(osv.Model):
    _inherit = "ir.ui.view"
    
    _columns = {
        'master_id':fields.many2one('ir.ui.view',string="Source View"),
        'version_ids': fields.one2many('ir.ui.view', 'master_id',string="Old Views"),
        'snapshot_id' : fields.many2one('website_version.snapshot',ondelete='cascade', string="Snapshot_id"),
    }

    _sql_constraints = [
        ('key_website_id_uniq', 'unique(key, snapshot_id, website_id)',
            'Key must be unique per snapshot.'),
    ]
    
    def write(self, cr, uid, ids, vals, context=None):
        #from pudb import set_trace; set_trace()
        if context is None:
            context = {}
        try:
            iter(ids)
        except:
            ids=[ids]

        experiment_id=context.get('experiment_id')
        if experiment_id and not context.get('mykey'):
            #from pudb import set_trace; set_trace()
            ctx = dict(context, mykey=True)
            exp = self.pool['website_version.experiment']
            experiment=exp.browse(cr, uid, [experiment_id], context=ctx)[0]
            for page_exp in experiment.experiment_page_ids:
                for id in ids:
                    if id in page_exp.view_id:
                        #from pudb import set_trace; set_trace()
                        context = dict(context, snapshot_id=page_exp.snapshot_id.id)
        
        #We write in a snapshot
        snapshot_id=context.get('snapshot_id')

        if snapshot_id and not context.get('mykey'):
            ctx = dict(context, mykey=True)
            snap = self.pool['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
            website_id=snapshot.website_id.id
            snapshot_date=snapshot.create_date
            snap_ids=[]
            no_snap_ids=[]
            for id in ids:
                check=True
                #The view corresponding to id is in the snapshot
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        snap_ids.append(view.id)
                        check=False
                #The view corresponding to id must be duplicated and inserted in the snapshot
                if check:
                    current = self.browse(cr, uid, [id], context=ctx)[0]
                    #To have a master view for this website
                    if not current.website_id:
                        id = self.copy(cr,uid, id,{'website_id':website_id},context=ctx)
                    copy_id=self.copy(cr,uid, id,{'master_id': id,'version_ids': None, 'snapshot_id':snapshot_id, 'website_id':website_id},context=ctx)
                    snap_ids.append(copy_id)
            super(ViewVersion, self).write(cr, uid, snap_ids, vals, context=ctx)
        else:
            ctx = dict(context, mykey=True)
            super(ViewVersion, self).write(cr, uid, ids, vals, context=ctx)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        if context is None:
            context = {}
        self.clear_cache()

        experiment_id=context.get('experiment_id')
        if experiment_id and not context.get('mykey'):
            ctx = dict(context, mykey=True)
            exp = self.pool['website_version.experiment']
            experiment=exp.browse(cr, uid, [experiment_id], context=ctx)[0]
            for page_exp in experiment.experiment_page_ids:
                for id in ids:
                    if id in page_exp.view_id:
                        context = dict(context, snapshot_id=page_exp.snapshot_id.id) 

        snapshot_id=context.get('snapshot_id')
        website_id=context.get('website_id')
        if snapshot_id and not context.get('mykey'):
            #from pudb import set_trace; set_trace()
            ctx = dict(context, mykey=True)
            snap = self.pool['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
            snap_ids=[]
            snap_trad={}
            for id in ids:
                check=True
                #The view corresponding to id is in the snapshot
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        snap_trad[view.id]=[view.master_id.id,view.master_id.xml_id,view.master_id.mode]
                        snap_ids.append(view.id)
                        check=False
                #The view corresponding to id is not in the snapshot
                if check:
                    snap_ids.append(id)        
            all_needed_views_snapshot= super(ViewVersion, self).read(cr, uid, snap_ids, fields=fields, context=ctx, load=load)

            for view in all_needed_views_snapshot:
                if view['id'] in snap_trad:
                    view['mode']=snap_trad[view['id']][2]
                    view['xml_id']=snap_trad[view['id']][1]
                    view['id']=snap_trad[view['id']][0]
            return all_needed_views_snapshot
        else:
            return super(ViewVersion, self).read(cr, uid, ids, fields=fields, context=context, load=load)
    
    #To make a snapshot of a snapshot
    def copy_snapshot(self,cr, uid, snapshot_id,new_snapshot_id, context=None):
        #from pudb import set_trace; set_trace()
        if context is None:
            context = {}
        ctx = dict(context, mykey=True)
        snap = self.pool['website_version.snapshot']
        snapshot=snap.browse(cr, uid, [snapshot_id],ctx)[0]
        for view in snapshot.view_ids:
            master_id=view.master_id.id
            copy_id=self.copy(cr,uid,view.id,{'master_id':master_id,'version_ids':None,'snapshot_id':new_snapshot_id},context=ctx)
            #super(ViewVersion, self).write(cr, uid, [copy_id], {'master_id':master_id,'snapshot_id':new_snapshot_id}, context=ctx)
            #super(ViewVersion, self).write(cr, uid,[master_id], {'version_ids': [(4, copy_id)]}, context=ctx)
            #snap.write(cr, uid,[new_snapshot_id], {'view_ids': [(4, copy_id)]}, context=ctx)

    #To publish a master view
    def action_publish(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        ctx = dict(context, mykey=True)
        snap = self.pool['website_version.snapshot']
        all_snapshot_ids = snap.search(cr, uid, [],context=context)
        all_snapshots = snap.browse(cr, uid, all_snapshot_ids, context=context)
        view_id = context.get('active_id')
        view = self.browse(cr, uid, [view_id],ctx)[0]
        key = view.key
        deleted_ids = self.search(cr, uid, [('key','=',key),('website_id','!=',False)],context=context)
        if view.website_id:
            master_id = self.search(cr, uid, [('key','=',key),('website_id','=',False),('snapshot_id','=',False)],context=context)[0]
            deleted_ids.remove(view.id)
            super(ViewVersion, self).write(cr, uid,[master_id], {'arch': view.arch}, context=ctx)
            self.unlink(cr, uid, deleted_ids, context=context)
        else:
            self.unlink(cr, uid, deleted_ids, context=context)

        
                