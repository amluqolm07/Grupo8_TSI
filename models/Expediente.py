# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Expediente(models.Model):
    
    _name = 'rrhh_upo.expediente'
    _description = 'Expediente'
    
    name = fields.Date(string='Fecha de apertura', help = "Fecha de apertura del expediente", required=True)
    fecha_fin = fields.Date(string='Fecha de cierre', help = "Fecha de cierre del expediente")
    estado = fields.Selection([('abierto', 'Abierto'),
                            ('cerrado', 'Cerrado')], required=True)