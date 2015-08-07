from openerp import models, fields

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    # TODO propose a merge to add this field by default in acount module
    sale_ids = fields.Many2many(comodel_name='sale.order',
                                relation='sale_order_invoice_rel',
                                column1='invoice_id',
                                column2='order_id',
                                string='Sale Orders')