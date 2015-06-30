from openerp import api
from openerp.osv import osv, fields
from pprint import pprint


class optibiz_saleorder(osv.osv):
    _inherit = 'sale.order'
    _name = 'sale.order'

    _columns = {
        'some_dummy_col': fields.char("Dummy")
    }

    @api.multi
    def _amount_all(self, field_name, args):
        price_list = self.partner_id.property_product_pricelist.id
        res = super(optibiz_saleorder, self)._amount_all(field_name, args)
        if price_list != 1:
            return res
        user = self.env.context.get('uid', False)
        if not user:
            return res

        logged_in = self.pool.get('res.users').browse(self.env.cr, self.env.uid, self.env.context['uid'],
                                                      self.env.context)
        cr = self.env.cr
        uid = logged_in.id
        option = -1
        sp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_selling_price')
        msp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_minimum_selling_price')
        csp = self.pool.get('res.users').has_group(cr, uid, 'miipl_msp.group_sell_on_coordinator_selling_price')
        if msp:
            option = 1
        elif sp:
            option = 0
        elif csp:
            option = 2
        for order in self:
            for line in order.order_line:
                product = line.product_id
                selling_price = product.lst_price
                if option == 1:
                    selling_price = product.min_selling_price
                elif option == 0:
                    selling_price = product.selling_price
                elif option == 2:
                    selling_price = product.coordinator_selling_price
                if line.price_unit < selling_price:
                    raise osv.except_osv("Error", "You can not give any discount greater than %f for %s" % (
                        selling_price, line.name))
        return res


optibiz_saleorder()
