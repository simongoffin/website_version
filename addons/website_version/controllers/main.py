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
                                    }, 
                                    context=context)
        return id_master
        
    @http.route(['/change_version'], type='json', auth="user", website=True)
    def set_version(self,id_version,id_seq):
        id_master=get_id(id_seq)
        request.session['id_version']=id_version
        request.session['id_master']=id_master
        return id_master
        
    @http.route(['/change_snapshot'], type='json', auth="user", website=True)
    def change_snapshot(self,snapshot_name):
        #from pudb import set_trace; set_trace()
        if snapshot_name=='Master':
            request.session['snapshot_id']=0
            #print 'SNAPSHOT ID={}'.format(request.session['snapshot_id'])
            return 'Master'
        else:
            cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
            snap = request.registry['website_version.snapshot']
            id=snap.search(cr, uid, [('name', '=', snapshot_name)])
            request.session['snapshot_id']=id[0]
            return id
        
    @http.route(['/create_snapshot'], type='json', auth="user", website=True)
    def create_snapshot(self,name):
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        snap = request.registry['website_version.snapshot']
        snapshot_id=request.session.get('snapshot_id')
        if snapshot_id==0 or snapshot_id==None:
            new_snapshot_id=snap.create(cr, uid,{'name':name}, context=context)
            request.session['snapshot_id']=new_snapshot_id
        else:
            iuv = request.registry['ir.ui.view']
            date=snap.browse(cr, uid, [snapshot_id], context)[0].create_date
            new_snapshot_id=snap.create(cr, uid,{'name':name,'create_date':date}, context=context)
            from pudb import set_trace; set_trace()
            iuv.copy_snapshot(cr, uid, snapshot_id,new_snapshot_id,context=context)
        return name
        
    @http.route(['/all_versions'], type='json', auth="public", website=True)
    def get_all_versions(self,id_seq):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        iuv = request.registry['ir.ui.view']
        id_view = get_id(id_seq)
#         request.session['id_version']=id_view
#         request.session['id_master']=id_view
        view=iuv.browse(cr, uid, [id_view], context)[0]
        current=view
        result=[]
        while current.master_id:
            result.append(current.master_id.id)
            current=current.master_id
        return result
    
    @http.route(['/all_snapshots'], type='json', auth="public", website=True)
    def get_all_snapshots(self):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        snap = request.registry['website_version.snapshot']
#         request.session['id_version']=id_view
#         request.session['id_master']=id_view
        ids=snap.search(cr, uid, [])
        result=snap.read(cr, uid, ids,['id','name','create_date'])
        res=[]
        res.append('Master')
        for ob in result:
            res.append(ob['name'])
        return res
        
    @http.route(['/write_snapshot'], type='json', auth="public", website=True)
    def get_qweb_number(self):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        iuv = request.registry['ir.ui.view']
        ids=iuv.search(cr, uid, [('type','=','qweb')],context=context)
        ob_list=iuv.browse(cr, uid, ids, context)
        result=0
        for ob in ob_list:
            result+=1
        snap_id=request.session.get('snapshot_id')
        if not snap_id==0 and not snap_id==None:
            #from pudb import set_trace; set_trace()
            iuv.write_snapshot(cr, uid, snap_id, context=context)
        return result
        
    @http.route(['/old_version/<value>'], type='http', auth="public", website=True)
    def get_version(self,value):
        print 'ID={}'.format(value)
        return value