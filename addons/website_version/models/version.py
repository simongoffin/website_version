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
        try:
            snapshot_id=request.session.get('snapshot_id')
        except:
            snapshot_id=None
        if snapshot_id and not context.get('mykey'):
            #from pudb import set_trace; set_trace()
            ctx = dict(context, mykey=True)
            snap = request.registry['website_version.snapshot']
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
            snapshot_date=snapshot.create_date
            snap_ids=[]
            no_snap_ids=[]
            #from pudb import set_trace; set_trace()
            for id in ids:
                check=True
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        snap_ids.append(view.id)
                        check=False
                if check:
                    current=self.browse(cr, uid, [id], context=ctx)
                    result_id=id
                    if current.version_ids:
                        #from pudb import set_trace; set_trace()
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
            if snapshot_id==0 and not context.get('mykey'):
                ctx = dict(context, mykey=True)
                #from pudb import set_trace; set_trace()
                for id in ids:
                    copy_id=self.copy(cr,uid,id,{'master_id':None,'version_ids':None},context=ctx)
                    super(ViewVersion, self).write(cr, uid,[copy_id], {'master_id': id}, context=ctx)
                    vals['version_ids'] = [(4, copy_id)]
                super(ViewVersion, self).write(cr, uid, ids, vals, context=ctx)
            else:
                ctx = dict(context, mykey=True)
                super(ViewVersion, self).write(cr, uid, ids, vals, context=ctx)
        
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        if context is None:
            context = {}
        self.clear_cache()
        try:
            snapshot_id=request.session.get('snapshot_id')
        except:
            snapshot_id=0
        if snapshot_id and not context.get('mykey'):
            #from pudb import set_trace; set_trace()
            snap = request.registry['website_version.snapshot']
            ctx = dict(context, mykey=True)
            snapshot=snap.browse(cr, uid, [snapshot_id], context=ctx)[0]
            snapshot_date=snapshot.create_date
            snap_ids=[]
            snap_trad={}
            for id in ids:
                check=True
                for view in snapshot.view_ids:
                    if view.master_id.id == id:
                        snap_trad[view.id]=[view.master_id.id,view.master_id.xml_id,view.master_id.mode]
                        snap_ids.append(view.id)
                        check=False
                if check:
                    current=self.browse(cr, uid, [id], context=ctx)[0]
                    result_id=id
                    check_two=True
                    if current.version_ids:
                        current_date=current.version_ids[0].create_date
                        for previous in current.version_ids:
                            #from pudb import set_trace; set_trace()
                            if previous.create_date>=snapshot_date:
                                result_id=previous.id
                                check_two=False
                                break
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
            
    def write_snapshot(self, cr, uid, snap_id, context=None):
        #from pudb import set_trace; set_trace()
        request.session['snapshot_id']=0
        self.clear_cache()
        ids=self.search(cr, uid, [('type','=','qweb')],context=context)
        ob_list=self.browse(cr, uid, ids, context=context)
        master_ids=[]
        for ob in ob_list:
            master_ids.append(ob.id)
        #from pudb import set_trace; set_trace()
        snap = request.registry['website_version.snapshot']
        snapshot=snap.browse(cr, uid, [snap_id], context=context)[0]
        snapshot_date=snapshot.create_date
        for id in master_ids:
            check=True
            check_b=True
            for view in snapshot.view_ids:
                if view.master_id.id==id:
                    #from pudb import set_trace; set_trace()
                    copy_id=self.copy(cr,uid,id,{'master_id':None,'version_ids':None},context=context)
                    super(ViewVersion, self).write(cr, uid,[copy_id], {'master_id': id}, context=context)
                    super(ViewVersion, self).write(cr, uid, id, {'arch':view.arch,'version_ids': [(4, copy_id)]}, context=context)
                    check=False
            if check:
                current=self.browse(cr, uid, [id], context=context)[0]
                if current.version_ids:
                    current_date=current.version_ids[0].create_date
                    for previous in current.version_ids:
                        if previous.create_date>=snapshot_date:
                            result_id=previous.id
                            copy_id=self.copy(cr,uid,id,{'master_id':None,'version_ids':None},context=context)
                            super(ViewVersion, self).write(cr, uid,[copy_id], {'master_id': id}, context=context)
                            super(ViewVersion, self).write(cr, uid, id, {'arch':previous.arch,'version_ids': [(4, copy_id)]}, context=context)
                            check_b=False
                            break

    def copy_snapshot(cr, uid, snapshot_id,new_snapshot_id, context=context):
        #from pudb import set_trace; set_trace()
        snap = request.registry['website_version.snapshot']
        snapshot=snap.browse(cr, uid, [snapshot_id], context=context)[0]
        #new_snapshot=snap.browse(cr, uid, [new_snapshot_id], context=ctx)[0]
        for view in snapshot.view_ids:
            copy_id=self.copy(cr,uid,view.id,{'master_id':None,'version_ids':None},context=context)
            super(ViewVersion, self).write(cr, uid, [copy_id], {'master_id':view.master_id.id,'snapshot_id':new_snapshot_id}, context=context)
            super(ViewVersion, self).write(cr, uid,[view.master_id.id], {'version_ids': [(4, copy_id)]}, context=context)
            snap.write(cr, uid,[new_snapshot_id], {'view_ids': [(4, copy_id)]}, context=context)
                


                    
                    