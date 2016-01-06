from openerp import models, api , osv
from datetime import datetime
from openerp.osv import fields

class optibiz_purchase_order_date(models.Model):
    _inherit = 'purchase.requisition'

    def _prepare_purchase_order(self, cr, uid, requisition, supplier, context=None):
        supplier_pricelist = supplier.property_product_pricelist_purchase
        return {
            'origin': requisition.name,
            'date_order': fields.datetime.now(),
            'partner_id': supplier.id,
            'pricelist_id': supplier_pricelist.id,
            'currency_id': supplier_pricelist and supplier_pricelist.currency_id.id or requisition.company_id.currency_id.id,
            'location_id': requisition.procurement_id and requisition.procurement_id.location_id.id or requisition.picking_type_id.default_location_dest_id.id,
            'company_id': requisition.company_id.id,
            'fiscal_position': supplier.property_account_position and supplier.property_account_position.id or False,
            'requisition_id': requisition.id,
            'notes': requisition.description,
            'picking_type_id': requisition.picking_type_id.id
        }
optibiz_purchase_order_date()