from . import test_website_version_base
from openerp.osv.orm import except_orm

class TestWebsiteVersionAll(test_website_version_base.TestWebsiteVersionBase):

    def test_read_with_right_context(self):
        """ Testing Read with right context """
        cr, uid, master_view_id, snapshot_id, arch_0_0_0_0= self.cr, self.uid, self.master_view_id, self.snapshot_id, self.arch_0_0_0_0

        result = self.ir_ui_view.read(cr, uid, [master_view_id], ['arch'], context={'snapshot_id':snapshot_id}, load='_classic_read')
        self.assertEqual(result[0]['arch'], arch_0_0_0_0, 'website_version: read: website_version must read the homepage_0_0_0_0 which is in the snapshot_0_0_0_0')

    def test_read_without_context(self):
        """ Testing Read without context """
        cr, uid, master_view_id, arch_master = self.cr, self.uid, self.master_view_id, self.arch_master

        result = self.ir_ui_view.read(cr, uid, [master_view_id], ['arch'], context=None, load='_classic_read')
        self.assertEqual(result[0]['arch'], arch_master, 'website_version: read: website_version must read the homepage which is in master')

    def test_read_with_wrong_context(self):
        """ Testing Read with wrong context """
        cr, uid, master_view_id, arch_master, wrong_snapshot_id = self.cr, self.uid, self.master_view_id, self.arch_master, 1234
        with self.assertRaises(except_orm):
            result = self.ir_ui_view.read(cr, uid, [master_view_id], ['arch'], context={'snapshot_id':wrong_snapshot_id}, load='_classic_read')

    def test_write_with_right_context(self):
        """ Testing Write with right context """
        cr, uid, master_view_id, view_0_0_0_0_id, snapshot_id, vals= self.cr, self.uid, self.master_view_id, self.view_0_0_0_0_id, self.snapshot_id, self.vals

        self.ir_ui_view.write(cr, uid, [master_view_id], vals, context={'snapshot_id':snapshot_id})
        view_0_0_0_0 = self.ir_ui_view.browse(cr, uid, [view_0_0_0_0_id], context={'snapshot_id':snapshot_id})[0]
        self.assertEqual(view_0_0_0_0.arch, vals['arch'], 'website_version: write: website_version must write (write test) on the homepage_0_0_0_0 which is in the snapshot_0_0_0_0')

    def test_write_without_context(self):
        """ Testing Write without context """
        cr, uid, master_view_id, view_0_0_0_0_id, snapshot_id, vals= self.cr, self.uid, self.master_view_id, self.view_0_0_0_0_id, self.snapshot_id, self.vals

        self.ir_ui_view.write(cr, uid, [master_view_id], vals, context=None)
        view_master = self.ir_ui_view.browse(cr, uid, [master_view_id], context=None)[0]
        self.assertEqual(view_master.arch, vals['arch'], 'website_version: write: website_version must write (write test) on the homepage which is in master')

    def test_write_with_wrong_context(self):
        """ Testing Write with wrong context """
        cr, uid, master_view_id, wrong_snapshot_id, vals= self.cr, self.uid, self.master_view_id, 1234, self.vals
        with self.assertRaises(except_orm):
            self.ir_ui_view.write(cr, uid, [master_view_id], vals, context={'snapshot_id':wrong_snapshot_id})

    def test_copy_snapshot(self):
        """ Testing Snapshot_copy"""
        cr, uid, view_0_0_0_0_id, snapshot_id, website_id = self.cr, self.uid, self.view_0_0_0_0_id, self.snapshot_id, self.website_id

        copy_snapshot_id = self.snapshot.create(cr, uid,{'name':'copy_snapshot_0_0_0_0', 'website_id':website_id}, context=None)
        self.ir_ui_view.copy_snapshot(cr, uid, snapshot_id,copy_snapshot_id,context=None)
        copy_snapshot = self.snapshot.browse(cr, uid, [copy_snapshot_id], context=None)[0]
        view_copy_snapshot=copy_snapshot.view_ids[0]
        view_0_0_0_0 = self.ir_ui_view.browse(cr, uid, [view_0_0_0_0_id], context={'snapshot_id':snapshot_id})[0]
        self.assertEqual(view_copy_snapshot.arch, view_0_0_0_0.arch, 'website_version: copy_snapshot: website_version must have in snpashot_copy the same views then in snapshot_0_0_0_0')

