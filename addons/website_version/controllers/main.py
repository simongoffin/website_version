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
    
    #To go back to old version
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
        iuv.write_simple(cr, uid,[id_view], {
                                        'arch': arch_master,
                                        #'master_id':master_id_master,
                                    }, 
                                    context=context)
        return id_master
        
    @http.route(['/all_versions'], type='json', auth="public", website=True)
    def get_all_versions(self,id_seq):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        iuv = request.registry['ir.ui.view']
        id_view = get_id(id_seq)
        view=iuv.browse(cr, uid, [id_view], context)[0]
        current=view
        result=[]
        while current.master_id:
            result.append(current.master_id.id)
            current=current.master_id
        return result
        
    @http.route(['/old_version/<value>'], type='http', auth="public", website=True)
    def get_version(self,value):
        print 'ID={}'.format(value)
        return value