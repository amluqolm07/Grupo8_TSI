# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Equipo_Investigacion(models.Model):
    
    _name = 'rrhh_upo.equipo_investigacion'
    _description = 'Equipo de Investigación'
    
    name = fields.Char(string='Equipo', help = "Equipo de investigación", required=True)
    especialidad = fields.Char(string='Especialidad', required=True)
    fecha_creacion = fields.Date(string='Fecha de creación', required=True)
    
    departamento_ids = fields.Many2many('rrhh_upo.departamento', String='Departamentos')
    
    equipo_trabaja_investigacion_ids = fields.One2many('rrhh_upo.equipo_trabaja_investigacion', 'equipo_investigacion_id', string='Equipo de investigación')