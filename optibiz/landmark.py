from openerp.osv import osv, fields

__author__ = 'santoshs'


class partner_landmark(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'landmark': fields.char('Landmark')
    }
    _defaults = {
        'landmark': ''
    }

partner_landmark()
