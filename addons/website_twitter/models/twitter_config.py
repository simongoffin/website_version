import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class twitter_config_settings(osv.osv_memory):
    _inherit = 'website'

    _columns = {
         
         'twitter_tutorial': fields.dummy(
                type="boolean", string="Show me how to obtain the Twitter API Key and Secret"),
    }
    
    def _check_twitter_authorization(self, cr, uid, config_id, context=None):
        website_config = self.browse(cr, uid, config_id, context=context)
        try:
            self.fetch_favorite_tweets(cr, uid, [website_config.website_id.id], context=context)
        except Exception:
            _logger.warning('Failed to verify twitter API authorization', exc_info=True)
            raise osv.except_osv(_('Twitter authorization error!'), _('Please double-check your Twitter API Key and Secret'))

    def create(self, cr, uid, vals, context=None):
        res_id = super(twitter_config_settings, self).create(cr, uid, vals, context=context)
        if vals.get('twitter_api_key') and vals.get('twitter_api_secret'):
            self._check_twitter_authorization(cr, uid, res_id, context=context)
        return res_id