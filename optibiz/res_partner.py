from openerp.osv import osv


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _defaults = {
        'user_id': lambda s, cr, uid, c: s._set_logged_in_user(cr,uid,c),
        'section_id': lambda s, cr, uid, c: s._set_logged_users_team(cr, uid, c)
    }

    def _set_logged_in_user(self, cr, uid, ctx=None):
        return uid

    def _set_logged_users_team(self, cr, uid, context=None):
        if context is None:
            context = {}
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return user.partner_id.section_id.id

res_partner()
