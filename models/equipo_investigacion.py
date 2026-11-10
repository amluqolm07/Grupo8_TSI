# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Equipo_Investigacion(models.Model):
    
    _name = 'rrhh_upo.equipo_investigacion'
    _description = 'Equipo de Investigación'
    
    name = fields.Char(string='Equipo', help = "Equipo de investigación", required=True)
    especialidad = fields.Char(string='Especialidad', required=True)
    
    equipo_investigacion_compone_departamento_ids = fields.One2many('rrhh_upo.equipo_investigacion_compone_departamento', 'equipo_investigacion_id', 'Departamentos del equipo de investigación')