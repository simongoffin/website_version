# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class ViewVersion(osv.Model):
    _inherit = "ir.ui.view"
    
    _columns = {
        'snapshot_id' : fields.many2one('website_version.snapshot',ondelete='cascade', string="Snapshot_id"),
    }

    _sql_constraints = [
        ('key_website_id_uniq', 'unique(key, snapshot_id, website_id)',
            'Key must be unique per snapshot.'),
    ]
    
    #To make a snapshot of a snapshot
    def copy_snapshot(self,cr, uid, snapshot_id,new_snapshot_id, context=None):
        if context is None:
            context = {}
        ctx = dict(context, mykey=True)
        snap = self.pool['website_version.snapshot']
        snapshot=snap.browse(cr, uid, [snapshot_id],ctx)[0]
        for view in snapshot.view_ids:
            copy_id=self.copy(cr,uid,view.id,{'snapshot_id':new_snapshot_id},context=ctx)

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

        
                