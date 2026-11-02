# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Entrevista(models.Model):

    _name = 'rrhh.upo.entrevista'
    _description = 'Entrevista'

    name = fields.Datetime(string='Fecha y hora de inicio',required=True, help='Rellene su fecha y hora de inicio')
    duracion = fields.Float(string='Duración (h)', default = 0.6)
    información_previa = fields.Text("Información previa", size = 400)
    apuntes = fields.Text("Apuntes post-entrevista", size = 400)
    fecha_hora_agendada = fields.Datetime('Fecha y hora agendada')
    resultado = fields.Selection([
        ('muy favorable','Muy favorable'),
        ('favorable','Favorable'),
        ('aceptable','Aceptable'),
        ('no aceptable','No aceptable')
        ('pendiente','Pendiente')
    ],'Resultado')
