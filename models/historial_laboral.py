# -*- coding: utf-8 -*-

from odoo import models, field, api

class Historial_laboral(models.Model):
    _name = 'rrhh_upo.historial.laboral'
    _description = 'Historial laboral'

    name = fields.Date(name='Fecha de inicio',required=True,help='Fecha en la que inició en el puesto')
    puesto = fields.Selection([
        ('personal tecnico','Personal Técnico'),
        ('pdi','PDI'),
        ('empleado externo','Empleado Externo'),
        ('rrhh','RRHH'),
    ],'Puesto')
    rol = fields.Char('Rol') # -*- PENDIENTE
    sueldo = fields.Float('Sueldo')
    fecha_fin = fields.Date('Fecha final')
    motivo_cambio = fields.Text('Motivo del cambio',size=240)
