# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sala(models.Model):

    _name = 'rrhh.upo.sala'
    _description = 'Sala'

    name = fields.Char(string='Nombre',required=True,size = 20, help='Rellene el nombre de la sala')
    edificio =fields.Integer('Edificio')
    planta = fields.Integer('Planta')
    direccion = fields.Integer('Dirección')
    aforo = fields.Integer('Aforo')
    superficie = fields.Float('Superficie (m^2)')
    altura = fields.Float('Altura (m)')
    hora_apertura = fields.Float('Apertura')
    hora_cierre = fields.Float('Cierre')
    estado = fields.Selection([
        ('disponible','Disponible'),
        ('ocupada','Ocupada'),
        ('mantenimiento','Mantenimiento'),
    ],'Estado')

    
