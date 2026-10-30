# -*- coding: utf-8 -*-
# from odoo import http


# class RrhhUpo(http.Controller):
#     @http.route('/rrhh__upo/rrhh__upo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rrhh__upo/rrhh__upo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rrhh__upo.listing', {
#             'root': '/rrhh__upo/rrhh__upo',
#             'objects': http.request.env['rrhh__upo.rrhh__upo'].search([]),
#         })

#     @http.route('/rrhh__upo/rrhh__upo/objects/<model("rrhh__upo.rrhh__upo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rrhh__upo.object', {
#             'object': obj
#         })

