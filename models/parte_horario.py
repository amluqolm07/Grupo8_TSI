# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Parte_horario(models.Model):
    _name = 'rrhh_upo.parte.horario'
    _description = 'Parte horario'

    name = fields.Datetime(name='Fecha y hora de entrada',required=True,help='Fecha y hora en la que entró al puesto')
    metodo_validacion= fields.Selection([
        ('firma digital','Firma digital'),
        ('firma biometrica','Firma biométrica'),
        ('firma manuscrita','Firma manuscrita'),
    ],'Método de validación',required=True)
    validado = fields.Boolean('Validado',default=False)
    fecha_hora_salida = fields.Datetime('Fecha y hora de la salida')
    incidencias = fields.Text('Incidencias/Justificaciones',size=240)
