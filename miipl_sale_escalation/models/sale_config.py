from openerp.osv import osv,fields
from datetime import date,datetime


class miipl_store_default_values(osv.osv):
    _name= 'miipl.store.default.values'
    _columns = {
        'name':fields.char('Quote escalation'),
        'hours':fields.integer('Hours'),

    }

    _defaults = {
        'hours': 24
    }

miipl_store_default_values()

class sale_config_settings(osv.osv_memory):
    _name = 'sale.config.settings'
    _inherit = 'sale.config.settings'
    _columns = {
    'sale_quote_escalation': fields.integer('Sale quote escalation ',default=10),
    }

    _defaults = {
        'sale_quote_escalation': 24
    }

    def get_default_sale_quote_escalation(self, cr, uid, fields, context=None):
        sale_escalation = self.pool.get('ir.model.data').get_object(cr, uid, 'miipl_sale_escalation', 'sale_quote_escalation')
        return {'sale_quote_escalation': sale_escalation.hours}

    def set_default_sale_quote_escalation(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        sale_escalation = self.pool.get('ir.model.data').get_object(cr, uid, 'miipl_sale_escalation', 'sale_quote_escalation')
        sale_escalation.write({'hours': config.sale_quote_escalation})

class miipl_sale_order(osv.osv):
    _name='sale.order'
    _inherit=['mail.thread', 'ir.needaction_mixin','sale.order']

    def run_sale_quote_scheduler(self, cr, uid, use_new_cursor=False, company_id = False, context=None):
        sale_orders = self.pool.get('sale.order').search(cr,uid,[])
        for quote_id in sale_orders:
            quote_details = self.pool.get('sale.order').browse(cr,uid,quote_id,context)
            current_date= datetime.strptime(fields.datetime.now(), '%Y-%m-%d %H:%M:%S')
            d2 =datetime.strptime(quote_details.write_date, '%Y-%m-%d %H:%M:%S')
            daysDiff = current_date-d2
            daysDiff=int(daysDiff.total_seconds()/(3600))
            sale_escalation = self.pool.get('ir.model.data').get_object(cr, uid, 'miipl_sale_escalation', 'sale_quote_escalation')
            if sale_escalation.hours <= daysDiff and quote_details.state in ('draft','quote_approved','sent'):
                if quote_details.section_id.user_id.id:
                    state=''
                    if quote_details.state == 'sent':
                        state='Quotation Sent'
                    elif quote_details.state == 'draft':
                        state='Approved'
                    elif quote_details.state == 'quote_approved':
                        state= 'Quotation Approved'
                    partner_id=self.pool.get('res.users').browse(cr,uid,quote_details.section_id.user_id.id,context).partner_id.id
                    hours=daysDiff%24
                    days=daysDiff/24
                    days=int(days)
                    user_list=[]
                    user_list.append(partner_id)
                    post_vars = {
                    'subject':quote_details.name,
                    'body': "The Sales Quote %s is in %s state since %d Days %d Hours."%(quote_details.name,state,days,hours),
                    'partner_ids': user_list,}
                    # thread_pool = self.pool.get('mail.thread')
                    self.message_post(
                    cr, uid, quote_details.id,
                    model='sale.order',
                    type="notification",
                    context=context,
                    **post_vars)

miipl_sale_order()