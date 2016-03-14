from openerp import osv, models
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from datetime import datetime, timedelta
from datetime import date
from openerp import SUPERUSER_ID

import warnings
import smtplib
from smtplib import SMTPException

class OptibizSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_wait(self,cr,uid,ids,context):
        order_id = self.pool.get('sale.order').browse(cr,uid,ids,context)
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval'  :

            logged_in = self.pool.get('res.users').browse(cr, uid, uid,
                                                      context)
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
                    raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s \n You can request for executive/manager approval" % (
                        selling_price, line.name))

        return super(OptibizSaleOrder, self).action_wait(cr,uid,ids,context)

    def _get_section_id(self,cr,uid,context = None):
        user_id = self.pool.get('res.users').browse(cr,uid,uid,context)
        return user_id.default_section_id.id

    _columns = {
        'date_confirm': fields.date('Confirmation Date', readonly=True, select=True, help="Date on which sales order is confirmed.", copy=False),
        'confirmed_uid': fields.many2one('res.users', 'Confirmed By', readonly=True),
        'reject_uid': fields.many2one('res.users', 'Rejected By', readonly=True),
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines',readonly=True, states={'draft': [('readonly', False)],'waiting_exec_approval': [('readonly', False)],'waiting_mgr_approval': [('readonly', False)]} ,copy=True),
        'section_id': fields.many2one('crm.case.section', 'Sales Team'),
        'edit_warning': fields.char('Note'),
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('waiting_exec_approval', 'Waiting Exec Approval'),
            ('waiting_mgr_approval', 'Waiting Manager Approval'),
            ('rejected','Rejected'),
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

    _defaults = {'section_id': _get_section_id,
                 'edit_warning': 'Editing this Quotation will move to draft'}




    def action_mgr_approve(self, cr, uid, ids, context=None):
         order_id=self.browse(cr,uid,ids,context)
         '''
         This function opens a window to compose an email, with the edi sale template message loaded by default
         '''
         assert len(ids) == 1, 'This option should only be used for a single id at a time.'
         ir_model_data = self.pool.get('ir.model.data')
         try:
            template_id = ir_model_data.get_object_reference(cr, uid,'miipl_wkf', 'email_template_manager_approval')[1]
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
            'mark_so_as_sent': False,
            'mark_so_as_exec_approval':False,
            'mark_so_as_manager_approval':True
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




    def action_exec_approve(self, cr, uid, ids, context=None):



         order_id=self.browse(cr,uid,ids,context)
         '''
         This function opens a window to compose an email, with the edi sale template message loaded by default
         '''
         assert len(ids) == 1, 'This option should only be used for a single id at a time.'
         ir_model_data = self.pool.get('ir.model.data')
         try:
            template_id = ir_model_data.get_object_reference(cr, uid,'miipl_wkf', 'email_template_exec_approval')[1]
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
            'mark_so_as_sent': False,
            'mark_so_as_exec_approval':True
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


    def action_quote_mgr_reject(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'rejected','reject_uid':uid}, context=context)
        return res


    def action_quote_reject(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'rejected','reject_uid':uid}, context=context)
        return res

    def action_update_quote(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return res

    def action_mgr_quote_approve(self,cr,uid,ids,context=None):
        order_id = self.browse(cr,uid,ids,context)
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
                    raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s" % (
                        selling_price, line.name))

        res = self.write(cr,uid,ids,{'state':'quote_approved','confirmed_uid':uid}, context=context)
        return res

    def action_quote_approve(self,cr,uid,ids,context=None):
        order_id = self.browse(cr,uid,ids,context)
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
                    raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s \n You can request for manager approval" % (
                        selling_price, line.name))

        res = self.write(cr,uid,ids,{'state':'quote_approved','confirmed_uid':uid}, context=context)
        return res

    def action_quotation_send(self, cr, uid, ids, context=None):

        order_id = self.browse(cr,uid,ids,context)
        user = order_id.env.context.get('uid', False)
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval' :
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
                        raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s \n You can request for for Executive/Manager approval" % (
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

    '''def write(self, cr, uid, ids, vals, context=None):

        print vals,'hi'
        xyz=self.check_product_price(cr,uid,ids,context)
        print xyz
        return super(OptibizSaleOrder, self).write(cr, uid, ids, vals,context)'''



    def print_quotation(self, cr, uid, ids, context=None):
        order_id = self.browse(cr,uid,ids,context)
        user = order_id.env.context.get('uid', False)
        if order_id.state == 'draft' or order_id.state == 'waiting_exec_approval' or order_id.state == 'waiting_mgr_approval' :
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
                        raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s \n You can request for for Executive/Manager approval" % (
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
            d1 = date.today()
            if product_obj.price_last_modified:
                d2 = datetime.strptime(product_obj.price_last_modified, '%Y-%m-%d').date()
                daysDiff = int(str((d1-d2).days))

                '''recordslist = self.pool.get('store.default.values').search(cr, uid, [])
                if recordslist:
                    for record in self.pool.get('store.default.values').browse(cr, uid, recordslist, context=context):
                        price_expiery_in_days = record.price_expiry_days
                print price_expiery_in_days, int(daysDiff)'''
                price_expiery_in_days = product_obj.price_expiry
                warning_msgs =''
                if daysDiff >= price_expiery_in_days:
                    warn_msg = ('Product price has been updated '+ str(daysDiff)+' days ago check with concerned person once .')
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
            raise osv.except_osv("Error", "You can not give any discount greater than %.2f for %s \n You can request for for Executive/Manager approval" % (
                        selling_price, line.name))

        return True

class mail_compose_message(osv.Model):
    _inherit = 'mail.compose.message'

    def send_mail(self, cr, uid, ids, context=None):

        print 'hi'
        context = context or {}
        if context.get('default_model') == 'sale.order' and context.get('default_res_id') and context.get('mark_so_as_sent') or context.get('mark_so_as_exec_approval') or context.get('mark_so_as_manager_approval'):
            context = dict(context, mail_post_autofollow=True)
            self.pool.get('sale.order').signal_workflow(cr, uid, [context['default_res_id']], 'quotation_sent')
            if context.get('mark_so_as_sent') == True:
               self.pool.get('sale.order').write(cr, uid, context['default_res_id'], {'state': 'sent'})
            if context.get('mark_so_as_exec_approval') == True:
               self.pool.get('sale.order').write(cr, uid, context['default_res_id'], {'state': 'waiting_exec_approval'})
            if context.get('mark_so_as_manager_approval') == True:
               self.pool.get('sale.order').write(cr, uid, context['default_res_id'], {'state': 'waiting_mgr_approval'})
        #return super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed. """
        context = dict(context or {})

        # clean the context (hint: mass mailing sets some default values that
        # could be wrongly interpreted by mail_mail)
        context.pop('default_email_to', None)
        context.pop('default_partner_ids', None)

        for wizard in self.browse(cr, uid, ids, context=context):
            mass_mode = wizard.composition_mode in ('mass_mail', 'mass_post')
            active_model_pool = self.pool[wizard.model if wizard.model else 'mail.thread']
            if not hasattr(active_model_pool, 'message_post'):
                context['thread_model'] = wizard.model
                active_model_pool = self.pool['mail.thread']

            # wizard works in batch mode: [res_id] or active_ids or active_domain
            if mass_mode and wizard.use_active_domain and wizard.model:
                res_ids = self.pool[wizard.model].search(cr, uid, eval(wizard.active_domain), context=context)
            elif mass_mode and wizard.model and context.get('active_ids'):
                res_ids = context['active_ids']
            else:
                res_ids = [wizard.res_id]

            batch_size = int(self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'mail.batch_size')) or self._batch_size

            sliced_res_ids = [res_ids[i:i + batch_size] for i in range(0, len(res_ids), batch_size)]
            for res_ids in sliced_res_ids:
                all_mail_values = self.get_mail_values(cr, uid, wizard, res_ids, context=context)
                for res_id, mail_values in all_mail_values.iteritems():
                    if wizard.composition_mode == 'mass_mail':
                        self.pool['mail.mail'].create(cr, uid, mail_values, context=context)
                    else:
                        subtype = 'mail.mt_comment'
                        if wizard.is_log or (wizard.composition_mode == 'mass_post' and not wizard.notify):  # log a note: subtype is False
                            subtype = False
                        if wizard.composition_mode == 'mass_post':
                            context = dict(context,
                                           mail_notify_force_send=False,  # do not send emails directly but use the queue instead
                                           mail_create_nosubscribe=True)  # add context key to avoid subscribing the author
                        id =active_model_pool.message_post(cr, uid, [res_id], type='comment', subtype=subtype, context=context, **mail_values)
                        # vinod code
                        if id:
                            temp=self.pool.get('mail.message').browse(cr,uid,id,context)
                            if temp.model=='sale.order':
                                order_id=self.pool.get('sale.order').search(cr,uid,[('name','=',temp.record_name)])
                                order=self.pool.get('sale.order').browse(cr,uid,order_id,context)
                                team_head=''
                                if order.state == 'waiting_exec_approval':
                                    team_head=order.section_id.user_id.partner_id
                                    cr.execute("select id from mail_notification where message_id=%s and partner_id=%s",(id,team_head.id,))
                                    result = cr.fetchone()
                                    if result:
                                        cr.execute("update mail_notification set starred = True where id =%s",(result[0],))
                                        #self.pool.get('mail.notification').write(cr,uid,result[0],{'starred':True})
                                if order.state == 'waiting_mgr_approval':
                                    team_head=order.section_id.parent_id.user_id.partner_id
                                    cr.execute("select id from mail_notification where message_id=%s and partner_id=%s",(id,team_head.id,))
                                    result = cr.fetchone()
                                    if result:
                                        cr.execute("update mail_notification set starred = True where id =%s",(result[0],))
                                #print self.pool.get('res.users').browse(cr,uid,team_head,context).partner_id
                        #vinod code end here
        return {'type': 'ir.actions.act_window_close'}

class res_partner(osv.osv):
    """ Inherits partner and adds CRM information in the partner form """
    _inherit = 'res.partner'
    _name = 'res.partner'

    def _get_section_id(self,cr,uid,context = None):
        user_id = self.pool.get('res.users').browse(cr,uid,uid,context)
        return user_id.default_section_id.id

    def _get_user_id(self,cr,uid,context = None):
        if context.get('search_default_customer'):
            return uid



    _columns = {
    'section_id': fields.many2one('crm.case.section', 'Sales Team'),
    'user_id':fields.many2one('res.users','Sale Person')

    }

    _defaults = {'section_id': _get_section_id,'user_id': _get_user_id}
res_partner()





class crm_lead(osv.osv):
    _name='crm.lead'
    _inherit='crm.lead'
    def run_scheduler(self, cr, uid, use_new_cursor=False, company_id = False, context=None):
        print 'Lead Scheduler'
        """lead_ids=self.pool.get('crm.lead').search(cr,uid,[],context)
        for lead_id in lead_ids:
            lead= self.pool.get('crm.lead').browse(cr,uid,lead_id,context)
            print lead.user_id.name,lead.section_id.name,lead.section_id.user_id.name
            partner_id=self.pool.get('res.users').browse(cr,uid,lead.section_id.user_id.id,context).partner_id.id
            user_list=[]
            user_list.append(partner_id)
            post_vars = {'subject': lead.name,
            'body': "Lead status is not update",
            'partner_ids': user_list,}
            thread_pool = self.pool.get('mail.thread')
            temp_id=thread_pool.message_post(
            cr, uid, False,
            type="notification",
            #subtype="mt_lead_create",
            context=context,
            **post_vars)

            template = self.pool.get('ir.model.data').get_object(cr, uid, 'crm', 'email_template_opportunity_reminder_mail')
            print template,partner_id
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, lead.section_id.user_id.id , force_send=True, context=context)
            print 'scheduler is running',temp_id,mail_id"""
crm_lead()