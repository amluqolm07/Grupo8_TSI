# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Equipo_Investigacion_Compone_Departamento(models.Model):
    
    _name = 'rrhh_upo.departamento'
    _description = 'Departamento'
    
    departamento_id = fields.Many2one('rrhh_upo.departamento', string='Departamento', required=True)
    equipo_investigacion_id = fields.Many2one('rrhh_upo.equipo_investigacion', string='Equipo de Investigación', required=True)
    