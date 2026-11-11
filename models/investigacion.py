# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Investigacion(models.Model):
    
    _name = 'rrhh_upo.investigacion'
    _description = 'Investigación'
    
    name = fields.Char(string='Nombre', help = "Nombre de la investigación", required=True)
    fecha_inicio = fields.Date(string='Fecha de inicio', required=True)
    fecha_fin = fields.Date(string='Fecha de fin')
    estado = fields.Selection([('en_proceso', 'En proceso'),
                            ('finalizado', 'Finalizado')], required=True)
    descripcion = fields.Text(string='Descripción', help = "Descripción de la investigación")
    # añadir financiacion total, suma de todas las financiaciones
    
    equipo_trabaja_investigacion_ids = fields.One2many('rrhh_upo.equipo_trabaja_investigacion', string='Equipo de investigación')
    
    