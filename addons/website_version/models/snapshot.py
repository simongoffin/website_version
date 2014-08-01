# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class Snapshot(osv.Model):
    _name = "website_version.snapshot"
    
    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        'create_date': fields.datetime('Create Date', readonly=True),
    }