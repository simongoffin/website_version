import openerp
from openerp import http
import simplejson
from openerp.http import request, serialize_exception as _serialize_exception
from cStringIO import StringIO
from collections import deque

def get_id(seq):
    debut='data-oe-id="'
    pos=seq.index(debut)
    pos+=len(debut)
    result=""
    while seq[pos] !='"':
        result+=(seq[pos])
        pos+=1
    return int(result)

class TableExporter(http.Controller):
    
    
    @http.route(['/request_rpc'], type='json', auth="public", website=True)
    def publish(self,id_seq):
        #from pudb import set_trace; set_trace()
#         cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
#         iuv = request.registry['ir.ui.view']
        id_view = get_id(id_seq)
#         view=iuv.browse(cr, uid, [id_view], context)[0]
#         for old_view in view.version_ids:
#             first=old_view
#             break
        
        return id_view