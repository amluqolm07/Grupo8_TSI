# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Telefonos_Departamentos(models.Model):
    
    _name = 'rrhh_upo.telefonos_departamentos'
    _description = 'Teléfonos de los Departamentos'
    
    name = fields.Integer(string='numero', help = "numero de telefono sin ", required=True)
    prefijo = fields.Integer(string='Prefijo', required=True)
    
    departamento_id = fields.Many2one('rrhh_upo.departamento', string='Departamento', required=True)