# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Solicitud(models.Model):
    
    _name = 'rrhh_upo.solicitud'
    _description = 'Solicitud'
    
    name = fields.Datetime(string='Fecha de solicitud', required=True)
    concepto = fields.Text()
    