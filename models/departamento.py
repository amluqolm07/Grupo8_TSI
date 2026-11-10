# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Departamento(models.Model):
    
    _name = 'grupo8_tsi.departamento'
    _description = 'Departamento'
    
    name = fields.Char(string='Nombre', help = "Nombre del departamento", required=True)
    telefono = fields.Integer(string='Teléfono', required=True)
    email = fields.Char(string='Email', required=True)