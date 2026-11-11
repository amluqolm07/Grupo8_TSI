# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Expediente(models.Model):
    
    _name = 'rrhh_upo.expediente'
    _description = 'Expediente'
    
    name = fields.Date(string='Fecha_apertura', help = "Fecha de apertura del expediente", required=True)
    fecha_fin = fields.Date('Fecha de cierre')
    estado = fields.Boolean('Abierto', required=True)
    # creditos matriculados atributo derivado
    
    grado_id = fields.Many2one('rrhh_upo.grado', string='Grado', required=True)