# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Equipo_Investigacion(models.Model):
    
    _name = 'grupo8_tsi.equipo_investigacion'
    _description = 'Equipo de Investigación'
    
    name = fields.Char(string='Equipo', help = "Equipo de investigación", required=True)
    especialidad = fields.Char(string='Especialidad', required=True)
    
    