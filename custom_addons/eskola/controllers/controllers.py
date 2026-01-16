# from odoo import http


# class Eskola(http.Controller):
#     @http.route('/eskola/eskola', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eskola/eskola/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eskola.listing', {
#             'root': '/eskola/eskola',
#             'objects': http.request.env['eskola.eskola'].search([]),
#         })

#     @http.route('/eskola/eskola/objects/<model("eskola.eskola"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eskola.object', {
#             'object': obj
#         })

