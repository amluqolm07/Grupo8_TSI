# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Investigacion(models.Model):
    
    _name = 'rrhh_upo.investigacion'
    _description = 'Investigación'
    
    name = fields.Char(string='Nombre', help = "Nombre de la investigación", required=True)
    fecha_inicio = fields.Date('Fecha de inicio', required=True)
    fecha_fin = fields.Date('Fecha de fin')
    estado = fields.Selection([('en_proceso', 'En proceso'),
                            ('finalizado', 'Finalizado')], required=True)
    descripcion = fields.Text()
    # añadir financiacion total, suma de todas las financiaciones
    
    equipo_trabaja_investigacion_ids = fields.One2many('rrhh_upo.equipo_trabaja_investigacion', 'investigacion_id', string='Equipo de investigación')
    
    