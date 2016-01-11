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


class product_price_validation(osv.osv):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'
    '''
    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
                                  uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                                  lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                                  flag=False, warehouse_id=False, context=None):
        context = context or {}
        product_uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        warning = {}
        # UoM False due to hack which makes sure uom changes price, ... in product_id_change
        res = self.product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                                     uom=False, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                                     lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
                                     fiscal_position=fiscal_position, flag=flag, context=context)

        if not product:
            res['value'].update({'product_packaging': False})
            return res



        # set product uom in context to get virtual stock in current uom
        if 'product_uom' in res.get('value', {}):
            # use the uom changed by super call
            context = dict(context, uom=res['value']['product_uom'])
        elif uom:
            # fallback on selected
            context = dict(context, uom=uom)

        # update of result obtained in super function
        product_obj = product_obj.browse(cr, uid, product, context=context)
        res['value'].update(
            {'product_tmpl_id': product_obj.product_tmpl_id.id, 'delay': (product_obj.sale_delay or 0.0)})

        # Calling product_packaging_change function after updating UoM
        res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging,
                                                    context=context)
        res['value'].update(res_packing.get('value', {}))
        warning_msgs = res_packing.get('warning') and res_packing['warning']['message'] or ''

        d1 = date.today()
        d2 = datetime.strptime(product_obj.sale_price_last_modified, '%Y-%m-%d').date()
        daysDiff = str((d1 - d2).days)
        price_expiery_in_days=self.pool.get('stock.config.settings').browse(cr, uid, uid, context=context).product_price_expiery_in_days
        print price_expiery_in_days,'hi',daysDiff
        if daysDiff >= 10:
            print 'hello'
            warn_msg = _('Product price has been updated ' + daysDiff + ' days ago check with concerned person once .')
            warning_msgs += _("Product Price ! : ") + warn_msg + "\n\n"

        if product_obj.type == 'product':
            # determine if the product needs further check for stock availibility
            is_available = self._check_routing(cr, uid, ids, product_obj, warehouse_id, context=context)

            # check if product is available, and if not: raise a warning, but do this only for products that aren't processed in MTO
            if not is_available:
                uom_record = False
                if uom:
                    uom_record = product_uom_obj.browse(cr, uid, uom, context=context)
                    if product_obj.uom_id.category_id.id != uom_record.category_id.id:
                        uom_record = False
                if not uom_record:
                    uom_record = product_obj.uom_id
                compare_qty = float_compare(product_obj.virtual_available, qty, precision_rounding=uom_record.rounding)
                if compare_qty == -1:
                    warn_msg = _(
                        'You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
                               (qty, uom_record.name,
                                max(0, product_obj.virtual_available), uom_record.name,
                                max(0, product_obj.qty_available), uom_record.name)
                    warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"

        # update of warning messages
        if warning_msgs:
            warning = {
                'title': _('Configuration Error!'),
                'message': warning_msgs
            }
        res.update({'warning': warning})
        return res

    '''


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

