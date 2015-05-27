# -*- coding: utf-8 -*-
from openerp import http

# class OptibizMsp(http.Controller):
#     @http.route('/optibiz_msp/optibiz_msp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/optibiz_msp/optibiz_msp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('optibiz_msp.listing', {
#             'root': '/optibiz_msp/optibiz_msp',
#             'objects': http.request.env['optibiz_msp.optibiz_msp'].search([]),
#         })

#     @http.route('/optibiz_msp/optibiz_msp/objects/<model("optibiz_msp.optibiz_msp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('optibiz_msp.object', {
#             'object': obj
#         })