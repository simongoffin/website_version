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
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        iuv = request.registry['ir.ui.view']
        id_view = get_id(id_seq)
        view=iuv.browse(cr, uid, [id_view], context)[0]
        id_master=view.master_id.id
        #recuperation des donnees du master
        master_view=iuv.browse(cr, uid, [id_master], context)[0]
        arch_master=master_view.arch
        master_id_master=master_view.master_id.id
        #print 'view_version_ids={}'.format(view.version_ids[0].id)
        print 'view_id={}'.format(view.id)
        print 'view_master_id={}'.format(view.master_id.id)
        print 'view_master_version_ids={}'.format(view.master_id.version_ids)
#         iuv.write_simple(cr, uid,[id_view], {
#                                         'arch': arch_master,
#                                         'master_id':master_id_master,
#                                     }, 
#                                     context=context)
        
        
#         for old_view in view.version_ids:
#             first=old_view
#             break
        return id_master