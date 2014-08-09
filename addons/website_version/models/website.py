# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class NewWebsite(osv.Model):
    _inherit = "website"

    _columns = {
        'snapshot_id':fields.many2one("website_version.snapshot",string="Snapshot"),
    }

    def get_current_snapshot(self,cr,uid,context=None):
        id=request.session.get('snapshot_id')
        if id=='Master' or id==None:
            return 'Master'
        else:
            ob=self.pool['website_version.snapshot'].browse(cr,uid,[id],context=context)
            return ob[0].name

    def get_current_website(self, cr, uid, context=None):
        #from pudb import set_trace; set_trace()
        website = super(NewWebsite,self).get_current_website(cr, uid, context=context)

        #key = 'website_%s_snapshot_id' % request.website.id
        key='snapshot_id'
        if request.session.get(key):
            request.context['snapshot_id'] = request.session.get(key)
        elif website.snapshot_id:
            request.context['snapshot_id'] = website.snapshot_id.id
            request.session['snapshot_id'] = website.snapshot_id.id

        return website
