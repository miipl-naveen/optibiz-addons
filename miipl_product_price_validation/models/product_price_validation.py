from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date



class product_template(osv.osv):
    _name = "product.template"
    _inherit = ['product.template']

    def price_expiry(self, cr, uid, ids, field_name, arg, context=None):
        res= {}
        for r in self.browse(cr, uid, ids, context):
            res[r.id] = {
            'product_expiers_in_days': 0
            }
            d1 = date.today()
            d2 = datetime.strptime(r.sale_price_last_modified, '%Y-%m-%d').date()
            product_expiers_in_days = str((d1 - d2).days)

            res[r.id]['product_expiers_in_days']= product_expiers_in_days

    _columns = {
        'price_expiry':fields.integer('Price Expires', required=True),
        'price_last_modified': fields.date('Price Last modified'),
        'product_expiers_in_days': fields.function(price_expiry,string='Product price Expiers in Days '),
    }
    _defaults ={'price_expiry':7

    }

    def create(self, cr, uid, vals, context=None):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        product_template_id = super(product_template, self).create(cr, uid, vals, context=context)
        related_vals = {}
        related_vals['price_last_modified'] = fields.datetime.now()
        self.write(cr, uid, product_template_id, related_vals, context=context)
        return product_template_id

    def write(self, cr, uid, ids, vals, context=None):
        ''' Store the standard price change in order to be able to retrieve the cost of a product template for a given date'''
        if type(ids) is int:
            ids=ids
        else:
            ids=ids[0]
        res = super(product_template, self).write(cr, uid, ids, vals, context=context)
        if 'list_price' in vals or 'coordinator_selling_price' in vals or 'selling_price' in vals or 'min_selling_price' in vals and 'standard_price' not in vals :
            self._set_standard_price(cr, uid, ids, 0, context=context)
        if 'list_price' in vals or 'coordinator_selling_price' in vals or 'selling_price' in vals or 'min_selling_price' in vals and 'standard_price' in vals :
            vals['price_last_modified'] = fields.datetime.now()
        return res


product_template()

