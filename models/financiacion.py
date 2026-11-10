# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Financiacion(models.Model):
    
    _name = 'rrhh_upo.financiacion'
    _description = 'Financiación'
    
    name = fields.Date(string='Fecha de acuerdpo', help = "Fecha de acuerdo de financiación", required=True)
    descripcion = fields.Text()
    
    