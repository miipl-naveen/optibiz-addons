from openerp import osv, models
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from datetime import datetime, timedelta
from datetime import date
import warnings
import smtplib
from smtplib import SMTPException

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
            ('shipping_except', 'Shipping Exception'),
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
         '''email_template_obj = self.pool.get('email.template')
         template_ids = email_template_obj.search(cr, uid, [('model_id.model', '=','sale.order')], context=context)
         print template_ids'''
         '''print uid
         team_id=self.pool.get('res.users').browse(cr,uid,uid,context).default_section_id
         team_lead=self.pool.get('crm.case.section').browse(cr,uid,team_id.id,context).user_id
         email_id=self.pool.get('res.users').browse(cr,uid,team_lead.id,context).login
         print email_id
         sender='vinod.k@madhuinfotech.com'
         receiver=str(email_id)
         message="You got approval request from your team member"
         try:
            smtpObj =  smtplib.SMTP(host='smtp.rediffmailpro.com', port=587)
            print 'line1',smtpObj
            #smtpObj.ehlo()
            print 'line2'
            #smtpObj.starttls()
            print 'line3',message
            #smtpObj.ehlo()
            username=sender
            pwd='Koushalya155'
            smtpObj.login(user=username, password=pwd)
            print 'line4'
            smtpObj.sendmail(sender,receiver,message)
            smtpObj.quit()
            #self.state='waiting'
            print "success"
         except smtplib.SMTPException:
            print "error" '''

         '''if template_ids:
              values = email_template_obj.generate_email(cr, uid, template_ids[0], ids[0], context=context)
              """values['subject'] = subject
              values['email_to'] = email_to
              values['body_html'] = body_html
              values['body'] = body_html"""
              values['email_to'] = email_id
              values['res_id'] = False
              mail_mail_obj = self.pool.get('mail.mail')
              msg_id = mail_mail_obj.create(cr, uid, values, context=context)
              print msg_id
              if msg_id:
                 mail_mail_obj.send(cr, uid, [msg_id], context=context)'''
         return True

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
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval':
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
            'state': order_id.state,
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

    def print_quotation(self, cr, uid, ids, context=None):
        order_id = self.browse(cr,uid,ids,context)
        user = order_id.env.context.get('uid', False)
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval':
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
                        raise osv.except_osv("Error", "You can not give any discount greater than %f for %s \n You can request for for Executive/Manager approval" % (
                            selling_price, line.name))

        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        #if order_id.state == 'quote_approved':
        #    self.signal_workflow(cr,uid,ids,'signal_approved_quote_sent')
        #    self.pool.get('sale.order').write(cr, uid, order_id.id, {'state': 'sent'})
        return self.pool['report'].get_action(cr, uid, ids, 'sale.report_saleorder', context=context)


class sale_order_line(osv.osv):

    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    _description = 'Sales Order Line'
    _columns = {

        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'), readonly=False),

    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                          flag=False, context=None):
        result = super(sale_order_line, self).product_id_change(cr, uid, ids,
                                                                  pricelist, product, qty, uom, qty_uos, uos, name,
                                                                  partner_id, lang, update_tax,
                                                                  date_order, packaging, fiscal_position, flag=True,context=context)
        if product:
            product_obj = self.pool.get('product.product').browse(cr,uid,product,context)
            print product_obj
            d1 = date.today()
            if product_obj.cost_price_last_modified:
                d2 = datetime.strptime(product_obj.cost_price_last_modified, '%Y-%m-%d').date()
            else :
                d2 = date.today()
            print d2
            daysDiff = str((d1-d2).days)
            price_expiery_in_days = 0
            recordslist = self.pool.get('store.default.values').search(cr, uid, [])
            if recordslist:
                for record in self.pool.get('store.default.values').browse(cr, uid, recordslist, context=context):
                    price_expiery_in_days = record.price_expiry_days
            print price_expiery_in_days, int(daysDiff)
            temp = int(daysDiff) - price_expiery_in_days
            warning_msgs =''
            print temp , 'temp'
            if temp > 0:
                warn_msg = ('Product price has been updated '+ daysDiff+' days ago check with concerned person once .')
                warning_msgs += ("Product Price ! : ") + warn_msg +"\n\n"
            warning={}
            if warning_msgs:
                warning = {
                       'title': ('Warning!'),
                       'message' : warning_msgs
                    }
            result.update({'warning': warning})


        result['value']['name'] = ' '
        return result

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

class mail_compose_message(osv.Model):
    _inherit = 'mail.compose.message'

    def send_mail(self, cr, uid, ids, context=None):
        context = context or {}
        if context.get('default_model') == 'sale.order' and context.get('default_res_id') and context.get('mark_so_as_sent'):
            context = dict(context, mail_post_autofollow=True)
            self.pool.get('sale.order').signal_workflow(cr, uid, [context['default_res_id']], 'quotation_sent')
            #if context.get('state') == 'quote_approved':
            #   self.pool.get('sale.order').write(cr, uid, context['default_res_id'], {'state': 'sent'})
        return super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)

