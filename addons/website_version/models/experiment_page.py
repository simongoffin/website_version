from openerp.osv import osv, fields


class Experiment_page(osv.Model):
    _name = "website_version.experiment_page"
    
    _columns = {
        'view_id': fields.many2one('ir.ui.view',string="View_id", required=True),
        'snapshot_id': fields.many2one('website_version.snapshot',string="Snapshot_id",required=True ),
        'experiment_id': fields.many2one('website_version.experiment',string="Experiment_id",required=True),
    }

    _sql_constraints = [
        ('view_experiment_uniq', 'unique(view_id, experiment_id)', 'You cannot have multiple records with the same view ID in the same experiment!'),
    ]