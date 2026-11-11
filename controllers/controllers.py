# -*- coding: utf-8 -*-
# from odoo import http


# class RrhhUpo(http.Controller):
#     @http.route('/rrhh_upo/rrhh_upo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rrhh_upo/rrhh_upo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rrhh_upo.listing', {
#             'root': '/rrhh_upo/rrhh_upo',
#             'objects': http.request.env['rrhh_upo.rrhh_upo'].search([]),
#         })

#     @http.route('/rrhh_upo/rrhh_upo/objects/<model("rrhh_upo.rrhh_upo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rrhh_upo.object', {
#             'object': obj
#         })

