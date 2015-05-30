from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class optibiz_product(osv.osv):
    _inherit = 'product.template'
    _columns = {
        'coordinator_selling_price': fields.float('Coordinator Selling Price', digits_compute=dp.get_precision('Product Price'), help="This is the price beyond which the sales person cannot give discounts"),
        'selling_price': fields.float('Executive Selling Price', digits_compute=dp.get_precision('Product Price'), help="This is the price beyond which the sales person cannot give discounts"),
        'min_selling_price': fields.float('Manager Selling Price', digits_compute=dp.get_precision('Product Price'), help="This is the price beyond which the sales manager cannot give discounts"),
    }
    _defaults = {
        'coordinator_selling_price': 0.0,
        'selling_price': 0.0,
        'min_selling_price': 0.0
    }



optibiz_product()
