from pprint import pprint
from openerp import osv, models, fields
from openerp import api


class product_attr(models.Model):
    # _inherit = 'product.template'
    _inherit = 'product.template'

    def copy(self, cr, uid, id, default=None, context=None):
        template = self.browse(cr, uid, id, context=context)
        default['attribute_line_ids'] = template['attribute_line_ids']
        old_res = super(product_attr, self).copy(cr, uid, id, default, context)
        new_product = self.browse(cr, uid, old_res, context=context)
        attributes = []
        for line in template['attribute_line_ids']:
            attr = [0, False, {'product_tmpl_id': new_product.id, 'attribute_id': line.attribute_id.id, 'value_ids': [[6, False, []]]}]
            attributes.append(attr)
        attrs = {'attribute_line_ids':attributes}
        res = self.write(cr, uid, [new_product.id], attrs, context=context)
        return old_res





        # product_attr()
