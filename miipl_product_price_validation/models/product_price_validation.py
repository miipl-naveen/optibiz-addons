from openerp.osv import osv
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import datetime, timedelta
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, \
    float_compare

from openerp import workflow
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

        # Vinod code
        'sale_price_last_modified': fields.date('Sale Price Last modified'),
        'cost_price_last_modified': fields.date('Cost Price Last Modified'),
        'product_expiers_in_days': fields.function(price_expiry,string='Product price Expiers in Days '),
    }

    def create(self, cr, uid, vals, context=None):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        product_template_id = super(product_template, self).create(cr, uid, vals, context=context)
        if not context or "create_product_product" not in context:
            self.create_variant_ids(cr, uid, [product_template_id], context=context)
        self._set_standard_price(cr, uid, product_template_id, vals.get('standard_price', 0.0), context=context)

        # TODO: this is needed to set given values to first variant after creation
        # these fields should be moved to product as lead to confusion
        related_vals = {}
        if vals.get('ean13'):
            related_vals['ean13'] = vals['ean13']
        if vals.get('default_code'):
            related_vals['default_code'] = vals['default_code']
        related_vals['sale_price_last_modified'] = fields.datetime.now()
        related_vals['cost_price_last_modified'] = fields.datetime.now()

        if related_vals:
            self.write(cr, uid, product_template_id, related_vals, context=context)

        return product_template_id

    def write(self, cr, uid, ids, vals, context=None):
        ''' Store the standard price change in order to be able to retrieve the cost of a product template for a given date'''
        if isinstance(ids, (int, long)):
            ids = [ids]
        if 'uom_po_id' in vals:
            new_uom = self.pool.get('product.uom').browse(cr, uid, vals['uom_po_id'], context=context)
            for product in self.browse(cr, uid, ids, context=context):
                old_uom = product.uom_po_id
                if old_uom.category_id.id != new_uom.category_id.id:
                    raise osv.except_osv(_('Unit of Measure categories Mismatch!'), _(
                        "New Unit of Measure '%s' must belong to same Unit of Measure category '%s' as of old Unit of Measure '%s'. If you need to change the unit of measure, you may deactivate this product from the 'Procurements' tab and create a new one.") % (
                                             new_uom.name, old_uom.category_id.name, old_uom.name,))
        # Vinod code
        if 'list_price' in vals:
            vals['sale_price_last_modified'] = fields.datetime.now()
        if 'standard_price' in vals:
            vals['cost_price_last_modified'] = fields.datetime.now()
        # vinod code ends here
        if 'standard_price' in vals:
            for prod_template_id in ids:
                self._set_standard_price(cr, uid, prod_template_id, vals['standard_price'], context=context)
        res = super(product_template, self).write(cr, uid, ids, vals, context=context)
        if 'attribute_line_ids' in vals or vals.get('active'):
            self.create_variant_ids(cr, uid, ids, context=context)
        if 'active' in vals and not vals.get('active'):
            ctx = context and context.copy() or {}
            ctx.update(active_test=False)
            product_ids = []
            for product in self.browse(cr, uid, ids, context=ctx):
                product_ids = map(int, product.product_variant_ids)
            self.pool.get("product.product").write(cr, uid, product_ids, {'active': vals.get('active')}, context=ctx)
        if 'list_price' in vals:
            vals['sale_price_last_modified'] = fields.datetime.now()
        if 'standard_price' in vals:
            vals['cost_price_last_modified'] = fields.datetime.now()
        return res


product_template()

