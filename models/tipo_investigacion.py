# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tipo_Investigacion(models.Model):
    
    _name = 'rrhh_upo.tipo_investigacion'
    _description = 'Tipo de Investigación'
    
    name = fields.Char(string='Tipo de Investigación', help = "Nombre del tipo de investigación", required=True)
    descriptor = fields.Char(string='Descriptor', required=True)
    
    