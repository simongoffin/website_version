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
        if context is None:
            context = {}
        try:
            iter(ids)
        except:
            ids=[ids]
        
        #We write in a snapshot
        version_name=context.get('version_name')
        print "VERSION NAME={}".format(version_name)
        if version_name and not context.get('mykey') and not version_name=='Master':
            ctx = dict(context, mykey=True)
            snap = request.registry['website_version.snapshot']
            snapshot_id=snap.search(cr, uid, [('name','=',version_name),])[0]
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
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
                    current=self.browse(cr, uid, [id], context=ctx)
                    result_id=id
                    if current.version_ids:
                        current_date=current.version_ids[0].create_date
                        for previous in current.version_ids:
                            if previous.create_date>=snapshot_date:
                                result_id=previous.id
                                break
                    copy_id=self.copy(cr,uid,result_id,{'master_id':None,'version_ids':None},context=ctx)
                    super(ViewVersion, self).write(cr, uid, copy_id, {'master_id':id,'snapshot_id':snapshot_id}, context=ctx)
                    super(ViewVersion, self).write(cr, uid,[id], {'version_ids': [(4, copy_id)]}, context=ctx)
                    snap.write(cr, uid,[snapshot_id], {'view_ids': [(4, copy_id)]}, context=ctx)
                    snap_ids.append(copy_id)
            super(ViewVersion, self).write(cr, uid, snap_ids, vals, context=context)
        else:
            # We write in master
            if version_name=='Master' and not context.get('mykey'):
                ctx = dict(context, mykey=True)
                #from pudb import set_trace; set_trace()
                for id in ids:
                    copy_id=self.copy(cr,uid,id,{'master_id':None,'version_ids':None},context=ctx)
                    super(ViewVersion, self).write(cr, uid,[copy_id], {'master_id': id}, context=ctx)
                    vals['version_ids'] = [(4, copy_id)]
                super(ViewVersion, self).write(cr, uid, ids, vals, context=ctx)
            else:
                # We launch the application
                ctx = dict(context, mykey=True)
                super(ViewVersion, self).write(cr, uid, ids, vals, context=ctx)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        if context is None:
            context = {}
        self.clear_cache()
        snapshot_id=context.get('snapshot_id')
        #print "READ CONTEXT ID={}".format(context.get('snapshot_id'))
        if snapshot_id==None:
            snapshot_id='Master'
        if not context.get('mykey') and not snapshot_id=='Master':
            ctx = dict(context, mykey=True)
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
            snapshot_date=snapshot.create_date
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
                #The view corresponding to id must be found with its create_date
                if check:
                    current=self.browse(cr, uid, [id], context=ctx)[0]
                    result_id=id
                    check_two=True
                    if current.version_ids:
                        current_date=current.version_ids[0].create_date
                        for previous in current.version_ids:
                            if previous.create_date>=snapshot_date:
                                result_id=previous.id
                                check_two=False
                                break
                    #The view corresponding to id is in master
                    if check_two:
                        snap_ids.append(id)
                    else:
                        master=self.browse(cr, uid, [id], context=ctx)[0]
                        snap_trad[result_id]=[master.id,master.xml_id,master.mode]
                        snap_ids.append(result_id)
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
        snap = request.registry['website_version.snapshot']
        snapshot=snap.browse(cr, uid, [snapshot_id],ctx)[0]
        for view in snapshot.view_ids:
            master_id=view.master_id.id
            copy_id=self.copy(cr,uid,view.id,{'master_id':None,'version_ids':None},context=ctx)
            super(ViewVersion, self).write(cr, uid, [copy_id], {'master_id':master_id,'snapshot_id':new_snapshot_id}, context=ctx)
            super(ViewVersion, self).write(cr, uid,[master_id], {'version_ids': [(4, copy_id)]}, context=ctx)
            snap.write(cr, uid,[new_snapshot_id], {'view_ids': [(4, copy_id)]}, context=ctx)
                