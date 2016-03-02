from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date

class produce_price_history(osv.osv):
    """
    Keep track of the ``product.template`` standard prices as they are changed.
    """
    _inherit = ['product.price.history']
    _name = 'product.price.history'
    _rec_name = 'datetime'
    _order = 'datetime desc'

    _columns = {
        'cost': fields.float('Cost Price'),
        'sale': fields.float('Sale Price'),
        'coordinator_selling_price': fields.float('Coordinator Price', help="This is the price beyond which the sales person cannot give discounts"),
        'selling_price': fields.float('Executive Price',  help="This is the price beyond which the sales person cannot give discounts"),
        'min_selling_price': fields.float('Manager Price', help="This is the price beyond which the sales manager cannot give discounts")
    }
produce_price_history()

class product_template(osv.osv):
    _name = "product.template"
    _inherit = ['mail.thread','product.template']
    _description = "Product Template"
    _order = "name"


    def _set_standard_price(self, cr, uid, product_tmpl_id, value, context=None):
        ''' Store the standard price change in order to be able to retrieve the cost of a product template for a given date'''
        if context is None:
            context = {}
        price_history_obj = self.pool['product.price.history']
        user_company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        company_id = context.get('force_company', user_company)
        p_id=self.browse(cr,uid,product_tmpl_id,context)
        cost_price = 0
        if value>0:
            cost_price =value
        else:
            cost_price = p_id.standard_price
        price_history_obj.create(cr, uid, {
            'product_template_id': product_tmpl_id,
            'cost': cost_price,
            'sale':p_id.list_price,
            'coordinator_selling_price':p_id.coordinator_selling_price,
            'selling_price':p_id.selling_price,
            'min_selling_price':p_id.min_selling_price,
            'company_id': company_id,
        }, context=context)

    def _get_price_history_ids(self, cr, uid, ids, field_name, arg, context=None):

        price_history = self.pool.get("product.price.history")
        res = {}
        for case in self.browse(cr,uid,ids,context):
            res[case.id] = price_history.search(cr, uid, [('product_template_id', '=', case.id)], order='id')
        print res,'hello'
        return res
    _columns = {
        'miipl_product_history': fields.function(_get_price_history_ids, method=True, type='one2many', obj='product.price.history', string='Product price history' ,readonly=True),
    }

product_template()