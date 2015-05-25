from openerp.osv import osv, fields


class product_category_with_attributes(osv.osv):
    _inherit = "product.category"
    _columns = {
        'attribute_ids': fields.many2many('product.attribute', id1='category_id', id2='product_id', string='Product Attributes'),
    }

product_category_with_attributes()
