# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Investigacion(models.Model):
    
    _name = 'grupo8_tsi.investigacion'
    _description = 'Investigación'
    
    name = fields.Char(string='Nombre', help = "Nombre de la investigación", required=True)
    fecha_inicio = fields.Datetime(string='Fecha de inicio', required=True, autodate=True)
    fecha_fin = fields.Datetime(string='Fecha de fin')
    estado = fields.Selection([('en_proceso', 'En proceso'),
                            ('finalizado', 'Finalizado')], required=True)
    
    