from openerp.osv import fields, osv
from datetime import date,datetime
import openerp.addons.decimal_precision as dp


class miipl_Product_Requisition(osv.osv):
    _name='miipl.product.requisition'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Request"
    _track = {
        'state': {
            'mt_request_created': lambda self, cr, uid, obj, ctx=None: obj.state in ['1draft','2cost_price_updated'],
            'mt_request_closed': lambda self, cr, uid, obj, ctx=None: obj.state in ['3done'],
        },
    }

    def _get_default_section_id(self, cr, uid, context=None):
        section_id = self.pool.get('res.users').browse(cr, uid, uid, context).default_section_id.id or False
        return section_id

    def _get_default_user_id(self, cr, uid, context=None):
        return uid

    _columns = {
        'date_done': fields.datetime('Confirmation Date', ),
        'name':fields.char('Name' ,readonly=True),
        'type':fields.selection([('new_product','Request for New Product Adding'),('price_update','Price Update')],'Request For',required=True,readonly=True, states={'1draft': [('readonly', False)]}),
        'note': fields.text('Description',readonly=True, states={'1draft': [('readonly', False)]}),
        'product_id': fields.many2one('product.template', 'Product',readonly=True, states={'1draft': [('readonly', False)]}),
        'create_date': fields.datetime('Date Created', readonly=True),
        'create_uid':  fields.many2one('res.users', 'Owner', readonly=True),
        'write_date': fields.datetime('Date Modified', readonly=True),
        'write_uid':  fields.many2one('res.users', 'Last Modification User', readonly=True),
        'price_last_modified': fields.char('Last Updated',readonly=True,store=True),
        'section_id': fields.many2one('crm.case.section', 'Sales Team',readonly=True, states={'1draft': [('readonly', False)]}),
        'user_id': fields.many2one('res.users', 'Salesperson', track_visibility='onchange',readonly=True, states={'1draft': [('readonly', False)]}),
        'manager_comment':fields.text('Manager Comment'),
        'state': fields.selection([
            ('1draft', 'Open'),
            ('2cost_price_updated', 'Cost Price Updated'),
            ('3done', 'Closed'),
            ],  'Status', select=True,readonly=True, copy=False,track_visibility='onchange')

    }


    _defaults = {'name': lambda obj, cr, uid, context: '/',
                 'type':'new_product',
                 'state':'1draft',
                 'user_id': _get_default_user_id,
                 'section_id': _get_default_section_id}

    def run_scheduler(self, cr, uid, use_new_cursor=False, company_id = False, context=None):
        product_idlist = self.pool.get('product.template').search(cr,uid,[])
        for product_id in product_idlist:
            product_details = self.pool.get('product.template').browse(cr,uid,product_id,context)
            d1 = date.today()
            if product_details.price_last_modified:
                d2 = datetime.strptime(product_details.price_last_modified, '%Y-%m-%d').date()
                if d1 == d2:
                    continue

                else:
                    daysDiff = int(str((d1-d2).days))
                    price_expiery_in_days = product_details.price_expiry
                    values = {}
                    if daysDiff >= price_expiery_in_days:
                        #values['name'] = self.pool['ir.sequence'].get(cr, uid, 'miipl.product.requisition', context=context) or '/'
                        values['type'] ='price_update'
                        values['product_id']=product_id
                        #values['user_id']= self._get_default_user_id,
                        #values['section_id']= self._get_default_section_id
                        var=self.pool.get('miipl.product.requisition').create(cr,uid,values,context)
        return True

    def action_new_product(self, cr, uid, ids, context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'miipl_product_price_validation', 'optibiz_product_template_form_view')
        view_id = view_ref and view_ref[1] or False,
        return {
            'name':'Product',
            'view_type':'form',
            'view_mode':'form',
            'views' : [(view_id[0],'form')],
            'res_model':'product.template',
            'view_id':view_id[0],
            'type':'ir.actions.act_window',
            'target':'new',
            'flags': {'form': {'action_buttons': True}}
        }

    def action_cost_price_updated(self, cr, uid, ids, context=None):
        '''if type(ids) is int:
            ids=ids
        else:
            ids=ids[0]
        PR_id=self.browse(cr,uid,ids,context)
        user_list=[]
        partner_id=self.pool.get('res.users',self).browse(cr,uid,PR_id.create_uid.id,context).partner_id.id
        user_list.append(partner_id)
        cr.execute("select id from res_groups where name='Product Manager'")
        res_groups_id= cr.fetchone()[0]
        cr.execute("select uid from res_groups_users_rel where gid = "+str(res_groups_id))
        for user_id in cr.fetchall():
            partner_id=self.pool.get('res.users',self).browse(cr,uid,user_id,context).partner_id.id
            user_list.append(partner_id)
        if PR_id.manager_comment:
            post_vars = {
             'subject':PR_id.name,
             'body': "Request as been updated %s"%(PR_id.manager_comment),
             'partner_ids': user_list,} # Where "4" adds the ID to the list
                                       # of followers and "3" is the partner ID
        else:
            post_vars = {
                'subject':PR_id.name,
             'body': "Request as been updated ",
             'partner_ids': user_list,}
        thread_pool = self.pool.get('mail.thread')
        thread_pool.message_post(
        cr, uid, PR_id.id,
        model='miipl.product.requisition',
        type="notification",
        subtype="mt_request_closed",
        context=context,
        **post_vars)'''
        self.write(cr,uid,ids,{'state':'2cost_price_updated'},context)

    def action_done(self, cr, uid, ids, context=None):
        if type(ids) is int:
            ids=ids
        else:
            ids=ids[0]
        PR_id=self.browse(cr,uid,ids,context)
        user_list=[]
        partner_id=self.pool.get('res.users',self).browse(cr,uid,PR_id.create_uid.id,context).partner_id.id
        user_list.append(partner_id)
        cr.execute("select id from res_groups where name='Product Manager'")
        res_groups_id= cr.fetchone()[0]
        cr.execute("select uid from res_groups_users_rel where gid = "+str(res_groups_id))
        for user_id in cr.fetchall():
            partner_id=self.pool.get('res.users',self).browse(cr,uid,user_id,context).partner_id.id
            user_list.append(partner_id)
        if PR_id.manager_comment:
            post_vars = {
             'subject':PR_id.name,
             'body': "Request as been updated %s"%(PR_id.manager_comment),
             'partner_ids': user_list,} # Where "4" adds the ID to the list
                                       # of followers and "3" is the partner ID
        else:
            post_vars = {
                'subject':PR_id.name,
             'body': "Request as been updated ",
             'partner_ids': user_list,}
        thread_pool = self.pool.get('mail.thread')
        thread_pool.message_post(
        cr, uid, PR_id.id,
        model='miipl.product.requisition',
        type="notification",
        subtype="mt_request_closed",
        context=context,
        **post_vars)
        self.write(cr,uid,ids,{'state':'3done','date_done':date.today()},context)


    def onchange_product_id(self, cr, uid, ids,product, context=None):
        pt_id=self.pool.get('product.template').browse(cr,uid,product,context)
        history_ids= self.pool.get('product.price.history').search(cr,uid,[('product_template_id', '=', product)],context)
        sp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_selling_price')
        msp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_minimum_selling_price')
        csp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_coordinator_selling_price')
        option=0
        if msp:
                option = 1
        elif sp:
                option = 2
        elif csp:
                option = 3
        if history_ids:
            history_id=self.pool.get('product.price.history').browse(cr,uid,history_ids[0],context)
            message="%s | Sale Price %s"%(history_id.create_date,pt_id.list_price)
            '''if option==1:
                message=message+" Manager Price %s"%(history_id.min_selling_price)
            elif option==2:
                message=message+" Executive Price %s"%(history_id.selling_price)
            elif option==3:
                message=message+" Co-ordinator Price %s"%(history_id.coordinator_selling_price)'''

            return {
                'value': {
                          'price_last_modified':message,

                          }
                }
        return True

    def onchange_type(self, cr, uid, ids, context=None):
        return {
                'value': {
                          'product_id':False,

                          }
                }
    def create(self, cr, uid, values, context=None):
        values['name'] = self.pool['ir.sequence'].get(cr, uid, 'miipl.product.requisition', context=context) or '/'
        id=super(miipl_Product_Requisition, self).create(cr, uid, values, context=context)
        PR_id=self.browse(cr,uid,id,context)
        user_list=[]
        partner_id=self.pool.get('res.users',self).browse(cr,uid,uid,context).partner_id.id
        user_list.append(partner_id)
        cr.execute("select id from res_groups where name='Product Manager'")
        res_groups_id= cr.fetchone()[0]
        cr.execute("select uid from res_groups_users_rel where gid = "+str(res_groups_id))
        for user_id in cr.fetchall():
            partner_id=self.pool.get('res.users',self).browse(cr,uid,user_id,context).partner_id.id
            user_list.append(partner_id)
        self.write(cr,uid,id,{'message_follower_ids':user_list})
        if PR_id.type == 'price_update':
            post_vars = {'subject': PR_id.name,
             'body': "Update Product Price",
             'partner_ids': user_list,}
        else:
            post_vars = {'subject': PR_id.name,
             'body': "Add Requested Product",
             'partner_ids': user_list,}
        thread_pool = self.pool.get('mail.thread')
        thread_pool.message_post(
        cr, uid, False,
        type="notification",
        subtype="mt_request_created",
        context=context,
        **post_vars)
        return id

    def _needaction_domain_get(self,cr,uid,context):
        """
        Show a count of sick horses on the menu badge.
        An exception: don't show the count to Bob,
        because he worries too much!
        """
        res_groups_id=[]
        cr.execute("select id from res_groups where name in ('Product Manager' ,'Product User')")

        for id in cr.fetchall():
            res_groups_id.append(id[0])
        res_groups_id=tuple(res_groups_id)
        cr.execute("select uid from res_groups_users_rel where gid in " + str(res_groups_id))
        for user_id in cr.fetchall():
            if user_id[0] == uid:
                return [('state', '=', '1draft')]
        return False
miipl_Product_Requisition()

class miipl_supplier_price(osv.osv):
    _name = 'miipl.supplier.price'
    _description = 'Supplier Price'
    _columns = {
        'name': fields.many2one('res.partner', 'Supplier', required=True,domain = [('supplier','=',True)], ondelete='cascade', help="Supplier of this product"),
        'product_t_id': fields.many2one('product.template', 'Product',),
        'cost': fields.float('Cost Price'),
        'create_date': fields.datetime('Date Created', readonly=True),
        'create_uid':  fields.many2one('res.users', 'Owner', readonly=True),
        'write_date': fields.datetime('Date Modified', readonly=True),
        'write_uid':  fields.many2one('res.users', 'Last Modification User', readonly=True),
    }
miipl_supplier_price()

class product_supplierinfo(osv.osv):
    _name = "product.supplierinfo"
    _inherit = "product.supplierinfo"
    _columns = {
        'cost':fields.float('Price' ,required=True),

    }

    def create(self, cr, uid, vals, context=None):
        supplier_price_obj = self.pool['miipl.supplier.price']
        supplier_price_obj.create(cr,uid,{'name':vals['name'],'product_t_id':vals['product_tmpl_id'],'cost':vals['cost']})
        supplier = super(product_supplierinfo, self).create(cr, uid, vals, context=context)
        return supplier

    def write(self, cr, uid, ids, vals, context=None):
        supplier = super(product_supplierinfo, self).write(cr, uid, ids, vals, context=context)
        supplier_price_obj = self.pool['miipl.supplier.price']
        if 'name' in vals or 'cost' in vals:
            temp=self.browse(cr,uid,ids,context)
            supplier_price_obj.create(cr,uid,{'name':temp.name.id,'product_t_id':temp.product_tmpl_id.id,'cost':temp.cost})
        return supplier
product_supplierinfo()

class product_template(osv.osv):
    _name = "product.template"
    _inherit = ['product.template']

    _columns = {
                'seller_price_history_ids': fields.one2many('miipl.supplier.price', 'product_t_id', 'Supplier Price',readonly=True),
                'standard_price': fields.property(type = 'float', digits_compute=dp.get_precision('Product Price'), readonly=True,
                                          help="Cost price of the product template used for standard stock valuation in accounting and used as a base price on purchase orders. "
                                               "Expressed in the default unit of measure of the product.",
                                          groups="base.group_user", string="Cost Price"),


                }
    def create(self, cr, uid, vals, context=None):
        min_cost=1111111111111
        for s_id in vals['seller_ids']:
            if s_id[2]['cost'] <= min_cost:
                min_cost = s_id[2]['cost']
        if min_cost != 1111111111111 :
            vals['standard_price']=min_cost
        #if not vals['seller_ids'] :
        #   raise osv.except_osv(('Warning!'),("Cannot create Product with out a supplier'."))
        product_template_id = super(product_template, self).create(cr, uid, vals, context=context)
        return product_template_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(product_template, self).write(cr, uid, ids, vals, context=context)
        product_details=self.browse(cr,uid,ids,context)
        old_cost=product_details.standard_price
        min_cost=111111111111
        for sel_id in product_details.seller_ids:
            if sel_id.cost <min_cost:
                min_cost = sel_id.cost
        if min_cost != 111111111111:
            if old_cost != min_cost:
                super(product_template, self).write(cr,uid,ids,{'standard_price':min_cost})
        return res
product_template()