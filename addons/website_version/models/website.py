# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class NewWebsite(osv.Model):
    _inherit = "website"

    _columns = {
        'snapshot_id':fields.many2one("website_version.snapshot",string="Snapshot", domain="[('website_id','=',context.get('active_id'))]")
    }

    def get_current_snapshot(self,cr,uid,context=None):
        snap = request.registry['website_version.snapshot']
        snapshot_id=request.context.get('snapshot_id')

        if not snapshot_id:
            request.context['snapshot_id'] = 0
            return (0, 'master')
        return snap.name_get(cr, uid, [snapshot_id], context=context)[0];

    def get_current_website(self, cr, uid, context=None):
        ids=self.search(cr, uid, [], context=context)
        url = request.httprequest.url
        
        websites = self.browse(cr, uid, ids, context=context)
        website = websites[0]
        for web in websites:
            if web.name in url:
                website = web
                break

        request.context['website_id'] = website.id

        if request.session.get('snapshot_id'):
            request.context['snapshot_id'] = request.session.get('snapshot_id')
        elif request.session.get('master'):
            request.context['snapshot_id'] = 0
        elif website.snapshot_id:
            request.context['snapshot_id'] = website.snapshot_id.id
        else:
            request.context['snapshot_id'] = 0
        

        return website