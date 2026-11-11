# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Material(models.Model):
    _name = 'rrhh_upo.material'
    _description = 'Material de la Oferta de Empleo'

    name = fields.Char(string="Material", required=True)
    cantidad = fields.Integer(string="Cantidad", default=1)
    descriptor = fields.Text(string="Especificaciones / Instrucciones / Observaciones", 
                             help='Detalla aquí las características técnicas, instrucciones y estado o condiciones de entrega de este material para la oferta.')

    oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo',string="Oferta de Empleo",required=True)