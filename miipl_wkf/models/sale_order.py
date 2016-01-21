from openerp import osv, models
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import warnings


class OptibizSaleOrder(models.Model):
    _inherit = 'sale.order'

    _columns = {
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines', copy=True),

        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('waiting_exec_approval', 'Waiting Exec Approval'),
            ('waiting_mgr_approval', 'Waiting Manager Approval'),
            ('quote_approved','Quote Approved'),
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

    def action_quote_reject(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return res

    def action_quote_approve(self,cr,uid,ids,context=None):
        order_id = self.browse(cr,uid,ids,context)
        print order_id
        price_list = order_id.partner_id.property_product_pricelist.id
        if price_list != 1:
            return res
        user = order_id.env.context.get('uid', False)
        if not user:
            return res

        logged_in = self.pool.get('res.users').browse(order_id.env.cr, order_id.env.uid, order_id.env.context['uid'],
                                                      order_id.env.context)
        cr = order_id.env.cr
        uid = logged_in.id
        option = -1
        sp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_selling_price')
        msp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_minimum_selling_price')
        csp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_coordinator_selling_price')
        if msp:
            option = 1
        elif sp:
            option = 0
        elif csp:
            option = 2
        for order in self.browse(cr,uid,ids,context):
            for line in order.order_line:
                product = line.product_id
                selling_price = product.lst_price
                if option == 1:
                    selling_price = product.min_selling_price
                elif option == 0:
                    selling_price = product.selling_price
                elif option == 2:
                    selling_price = product.coordinator_selling_price
                if line.price_unit < selling_price:
                    raise osv.except_osv("Error", "You can not give any discount greater than %f for %s \n You can request for manager approval" % (
                        selling_price, line.name))

        res = self.write(cr,uid,ids,{'state':'quote_approved'}, context=context)
        return res

    def action_quotation_send(self, cr, uid, ids, context=None):

        order_id = self.browse(cr,uid,ids,context)
        user = order_id.env.context.get('uid', False)
        print order_id.state
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval':
            if not user:
                return res
            print 'hi'
            logged_in = self.pool.get('res.users').browse(order_id.env.cr, order_id.env.uid, order_id.env.context['uid'],
                                                      order_id.env.context)
            cr = order_id.env.cr
            uid = logged_in.id
            option = -1
            sp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_selling_price')
            msp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_minimum_selling_price')
            csp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_coordinator_selling_price')
            if msp:
                option = 1
            elif sp:
                option = 0
            elif csp:
                option = 2
            for order in self.browse(cr,uid,ids,context):
                for line in order.order_line:
                    product = line.product_id
                    selling_price = product.lst_price
                    if option == 1:
                        selling_price = product.min_selling_price
                    elif option == 0:
                        selling_price = product.selling_price
                    elif option == 2:
                        selling_price = product.coordinator_selling_price
                    if line.price_unit < selling_price:
                        raise osv.except_osv("Error", "You can not give any discount greater than %f for %s \n You can request for for Executive/Manager approval" % (
                            selling_price, line.name))

        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'sale.order',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class sale_order_line(osv.osv):

    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    _description = 'Sales Order Line'
    _columns = {

        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'), readonly=False),

    }
    def price_validation(self, cr, uid, ids,product_id, context=None):


        user = order_id.env.context.get('uid', False)
        if not user:
            return res

        logged_in = self.pool.get('res.users').browse(order_id.env.cr, order_id.env.uid, order_id.env.context['uid'],
                                                      order_id.env.context)
        option = -1
        sp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_selling_price')
        msp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_minimum_selling_price')
        csp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_coordinator_selling_price')
        if msp:
            option = 1
        elif sp:
            option = 0
        elif csp:
            option = 2

        product = product_id
        selling_price = product.lst_price
        if option == 1:
            selling_price = product.min_selling_price
        elif option == 0:
            selling_price = product.selling_price
        elif option == 2:
            selling_price = product.coordinator_selling_price
        if line.price_unit < selling_price:
            raise osv.except_osv("Error", "You can not give any discount greater than %f for %s \n You can request for for Executive/Manager approval" % (
                        selling_price, line.name))

        return True

