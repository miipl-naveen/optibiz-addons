from openerp import api
from openerp.osv import osv, fields


class partner_landmark(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'landmark': fields.char('Landmark')
    }
    _defaults = {
        'landmark': ''
    }

    @api.multi
    def write(self, values):
        res = super(partner_landmark, self).write(values)
        domain = [
            ('partner_id.id', '=', self.id)
        ]
        user = self.env['res.users'].search(domain)
        if not user:
            return res
        domain = [
            ('user_id.id', '=', user.id)
        ]
        companies = self.env['res.partner'].search(domain)
        for company in companies:
            company.write({'section_id': self.section_id.id})
        return res


partner_landmark()
