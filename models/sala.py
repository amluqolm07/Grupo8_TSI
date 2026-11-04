# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sala(models.Model):

    _name = 'rrhh_upo.sala'
    _description = 'Sala'

    name = fields.Integer(string='Número',required=True,help='Rellene el número de la sala')
    planta = fields.Integer('Planta')
    aforo = fields.Integer('Aforo')
    superficie = fields.Float('Superficie (m^2)')
    altura = fields.Float('Altura (m)')
    hora_apertura = fields.Float('Hora de apertura')
    hora_cierre = fields.Float('Hora de cierre')
    estado = fields.Selection([
        ('disponible','Disponible'),
        ('ocupada','Ocupada'),
        ('mantenimiento','Mantenimiento'),
    ],'Estado')

    
