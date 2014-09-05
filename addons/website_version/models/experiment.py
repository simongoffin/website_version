# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class Experiment(osv.Model):
    _name = "website_version.experiment"
    
    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        'experiment_page_ids': fields.one2many('website_version.experiment_page', 'experiment_id',string="page_ids"),
        'website_id': fields.many2one('website',string="Website", required=True),
        
    }