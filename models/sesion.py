# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sesion(models.Model):

    _name = 'rrhh.upo.sesion'
    _description = 'Sesion'

    name = fields.Datetime(string='Fecha y hora de inicio',required=True, help='Rellene su fecha y hora de inicio')
    duracion = fields.Float(string='Duración (h)', default = 1)
    incidencias = fields.Text("Incidencias")
    asistentes_previstos = fields.Integer("Asistentes previstos")
    asistentes_reales = fields.Integer("Asistentes reales")
    grabada = fields.Boolean('Sesion grabada', default=False)
    estado = fields.Selection([
            ('pendiente','Pendiente'),
            ('finalizada','Finalizada'),
            ('cancelada','Cancelada'),
        ],'Estado')