# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Grado(models.Model):
    
    _name = 'rrhh_upo.grado'
    _description = 'Grado'
    
    name = fields.Char(string='ID', help = "ID del grado", required=True)
    nombre = fields.Char(string='Nombre', help = "Nombre del grado", required=True)
    rama = fields.Selection([('ingenieria', 'Ingeniería'),
                             ('ciencias', 'Ciencias'),
                             ('humanidades', 'Humanidades'),
                             ('salud', 'Salud'),
                             ('sociales', 'Sociales')], required=True)
    
    asignatura_ids = fields.One2many('rrhh_upo.asignatura', 'grado_id', 'Asignaturas del grado')
    
    
    