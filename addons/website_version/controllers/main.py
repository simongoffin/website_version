import openerp
from openerp import http
import simplejson
from openerp.http import request, serialize_exception as _serialize_exception
from cStringIO import StringIO
from collections import deque
import datetime

class TableExporter(http.Controller):
        
    @http.route(['/change_snapshot'], type='json', auth="user", website=True)
    def change_snapshot(self,snapshot_name):
        #from pudb import set_trace; set_trace()
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        #website_object = request.registry['website']
        #my_website = website_object.get_current_website(self, cr, uid, context=context)

        if snapshot_name=='Master':
            request.session['snapshot_id']='Master'
            #request.session['website_%s_snapshot_id'%(my_website.id)]=0
            return 'Master'
        else:
            cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
            snap = request.registry['website_version.snapshot']
            id=snap.search(cr, uid, [('name', '=', snapshot_name)],context=context)
            request.session['snapshot_id']=id[0]
            #request.session['website_%s_snapshot_id'%(my_website.id)]=id[0]
            return id

    @http.route(['/create_snapshot'], type='json', auth="user", website=True)
    def create_snapshot(self,name):
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        if name=="":
            name=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        snap = request.registry['website_version.snapshot']
        snapshot_id=request.session.get('snapshot_id')
        if snapshot_id=='Master' or snapshot_id==None:
            new_snapshot_id=snap.create(cr, uid,{'name':name}, context=context)
            request.session['snapshot_id']=new_snapshot_id
        else:
            iuv = request.registry['ir.ui.view']
            date=snap.browse(cr, uid, [snapshot_id], context=context)[0].create_date
            new_snapshot_id=snap.create(cr, uid,{'name':name,'create_date':date}, context=context)
            iuv.copy_snapshot(cr, uid, snapshot_id,new_snapshot_id,context=context)
            request.session['snapshot_id']=new_snapshot_id
        return name

    @http.route(['/delete_snapshot'], type='json', auth="user", website=True)
    def delete_snapshot(self):
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        snap = request.registry['website_version.snapshot']
        snapshot_id=request.session.get('snapshot_id')
        if not snapshot_id=='Master':
            name=snap.browse(cr,uid,[snapshot_id],context=context).name
            snap.unlink(cr, uid, [snapshot_id], context=context)
            request.session['snapshot_id']='Master'
        else:
            name="nothing"
        return name
    
    @http.route(['/all_snapshots'], type='json', auth="public", website=True)
    def get_all_snapshots(self):
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        snap = request.registry['website_version.snapshot']
        ids=snap.search(cr, uid, [])
        result=snap.read(cr, uid, ids,['id','name','create_date'],context=context)
        res=[]
        res.append('Master')
        for ob in result:
            res.append(ob['name'])
        return res


    @http.route(['/set_context'], type='json', auth="public", website=True)
    def set_context(self):
        cr, uid, context = request.cr, openerp.SUPERUSER_ID, request.context
        snapshot_id=request.session.get('snapshot_id')
        print 'OK={}'.format(snapshot_id)
        
        return snapshot_id
