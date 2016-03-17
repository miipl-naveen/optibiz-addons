from openerp.osv import orm

class Website(orm.Model):
	_inherit = "website"

	def sale_product_domain(self, cr, uid, ids, context=None):
		domain = super(Website, self).sale_product_domain(cr, uid, ids, context=context)
		return domain
		if uid != 3:
			domain = ['&'] + domain + [("qty_available", "=", True)]
		return domain