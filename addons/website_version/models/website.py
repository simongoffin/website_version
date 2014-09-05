# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class NewWebsite(osv.Model):
    _inherit = "website"

    _columns = {
        'experiment_id':fields.many2one("website_version.experiment",string="Experiment", domain="[('website_id','=',context.get('active_id'))]")
    }

    def get_current_snapshot(self,cr,uid,context=None): 
        #from pudb import set_trace; set_trace()
        snap = request.registry['website_version.snapshot']
        snapshot_id=request.context.get('snapshot_id')

        if request.context.get('experiment_id'):
            return (0, 'Experiment')

        if not snapshot_id:
            request.context['snapshot_id'] = 0
            return (0, 'master')
        return snap.name_get(cr, uid, [snapshot_id], context=context)[0];

    def get_current_experiment(self,cr,uid,context=None): 
        #from pudb import set_trace; set_trace()
        if request.session.get('Experiment'):
            return self.get_current_website(cr, uid, context=context).experiment_id.id
        else:
            return 0

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

        #key = 'website_%s_snapshot_id' % request.website.id
        if request.session.get('snapshot_id'):
            request.context['snapshot_id'] = request.session.get('snapshot_id')
        elif request.session.get('Master'):
            request.context['snapshot_id'] = 0
        elif website.experiment_id and request.session.get('Experiment'):
            request.context['experiment_id'] = website.experiment_id.id
        elif website.experiment_id:
            request.context['experiment_id'] = website.experiment_id.id
        else:
            request.context['snapshot_id'] = 0
        

        return website