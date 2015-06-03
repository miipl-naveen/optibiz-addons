from openerp import osv, models
from openerp.osv import fields, osv


class OptibizSaleOrder(models.Model):
    _inherit = 'sale.order'

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('waiting_exec_approval', 'Waiting Exec Approval'),
            ('waiting_mgr_approval', 'Waiting Manager Approval'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
    }


    def action_mgr_approve(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'waiting_mgr_approval'}, context=context)
        return res

    def action_exec_approve(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'waiting_exec_approval'}, context=context)
        return res
