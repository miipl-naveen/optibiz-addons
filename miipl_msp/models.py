from openerp import api
from openerp.osv import osv, fields
import warnings
from pprint import pprint


class optibiz_saleorder(osv.osv):
    _inherit = 'sale.order'
    _name = 'sale.order'

    _columns = {
        'some_dummy_col': fields.char("Dummy")
    }

optibiz_saleorder()
