# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp.http import request


class NewWebsite(osv.Model):
    _inherit = "website"


    def get_current_snapshot(self,cr,uid,context=None):
        id=request.session.get('snapshot_id')
        return self.pool['snapshot'].browse(cr,uid,[id],context=context)