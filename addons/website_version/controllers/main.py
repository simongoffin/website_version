import openerp
from openerp import http
import simplejson
from openerp.http import request, serialize_exception as _serialize_exception
from cStringIO import StringIO
from collections import deque

class VersionRequest(http.Controller):


    @http.route(['/request_rpc'], type='json', auth="public", website=True)
    def publish(self, xml_id):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        iuv = request.registry['ir.ui.view']
        mimetype ='application/xml;charset=utf-8'
        
        view_id=iuv.search(cr, uid, [
            ('xml_id', '=', int(xml_id)),],context=request.context)
        view=iuv.browse(cr, uid, [view_id], context=None)
        for old_view in view.version_ids:
            return old_view.arch