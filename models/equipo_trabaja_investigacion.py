# -*- coding: utf-8 -*-

from odoo import models, fields, api

class equipo_trabaja_investigacion(models.Model):
    
    _name = 'rrhh_upo.equipo_trabaja_investigacion'
    _description = 'Equipo de Investigación'
    
    fecha_anexion = fields.Date(string='Fecha de anexión', help = "Fecha de anexión del equipo a la investigación", required=True)
    presupuesto = fields.Float('Presupuesto', required=True)
    
    equipo_investigacion_id = fields.Many2one('rrhh_upo.equipo_investigacion', string='Equipo de investigación', required=True)
    investigacion_id = fields.Many2one('rrhh_upo.investigacion', string='Investigacion', required=True)

