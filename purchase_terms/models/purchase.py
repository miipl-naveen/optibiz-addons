from openerp.osv import osv,fields

class res_company(osv.Model):
    _inherit = "res.company"
    _columns = {
        'purchase_note': fields.text('Default Purchase Terms and Conditions', translate=True, help="Default terms and conditions for purchases."),
    }

class purchase_order(osv.Model):
	_inherit = "purchase.order"
	_columns = {
		'notes': fields.text('Terms and conditions', required=True),
	}
	_defaults = {
		'notes': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.purchase_note,
	}

class purchase_requisition(osv.Model):
	_inherit = "purchase.requisition"
	_columns = {
		'description': fields.text('Description', required=True)
	}
	_defaults = {
		'description': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.purchase_note,
	}
