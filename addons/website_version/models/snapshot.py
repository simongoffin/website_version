# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class Snapshot(osv.Model):
    _name = "website_version.snapshot"
    
    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        #Relational
        'view_ids' : fields.many2many('ir.ui.view',string="Snapshot views"),
    }