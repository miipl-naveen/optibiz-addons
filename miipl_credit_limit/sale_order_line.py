from openerp.osv import osv


class sale_order_line_empty_name(osv.osv):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                          flag=False, context=None):
        result = super(sale_order_line_empty_name, self).product_id_change(cr, uid, ids,
                                                                  pricelist, product, qty, uom, qty_uos, uos, name,
                                                                  partner_id, lang, update_tax,
                                                                  date_order, packaging, fiscal_position, flag=True,
                                                                  context=context)
        result['value']['name'] = ' '
        return result


sale_order_line_empty_name()
