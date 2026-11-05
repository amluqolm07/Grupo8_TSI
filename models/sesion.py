# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Sesion(models.Model):

    _name = 'rrhh_upo.sesion'
    _description = 'Sesion'
    _rec_name = 'fecha_hora_inicio'

    fecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio',required=True, help='Rellene su fecha y hora de inicio')
    duracion = fields.Float(string='Duración (h)', default = 1)
    incidencias = fields.Text("Incidencias",size = 240)
    asistentes_previstos = fields.Integer("Asistentes previstos")
    asistentes_reales = fields.Integer("Asistentes reales")
    grabada = fields.Boolean('Sesion grabada', default=False)
    estado = fields.Selection([
            ('pendiente','Pendiente'),
            ('finalizada','Finalizada'),
            ('cancelada','Cancelada'),
        ],'Estado')

    fecha_hora_final = fields.Datetime('Fecha y hora en la que acaba la sesion', compute='calcular_fecha_hora_final')

    #Final = inicio + duración
    @api.depends('fecha_hora_inicio','duracion')
    def calcular_fecha_hora_final(self):
        for record in self:
            if record.duracion and record.fecha_hora_inicio:
                record.fecha_hora_final = record.fecha_hora_inicio + timedelta(hours=record.duracion)
            else:
                record.fecha_hora_final = False

    #No puede durar menos de 0 horas
    @api.constrains('duracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.duracion <= 0:
                raise ValidationError('La duración de la sesión debe ser un valor positivo')

    #Ninguna asistencia menor a 0
    @api.constrains('asistentes_previstos', 'asistentes_reales')
    def _check_asistentes(self):
        for record in self:
            if record.asistentes_previstos and record.asistentes_previstos < 0:
                raise ValidationError('Los asistentes previstos no pueden ser negativos')
            if record.asistentes_reales and record.asistentes_reales < 0:
                raise ValidationError('Los asistentes reales no pueden ser negativos')

    #No puede terminar sin saber cuantos han ido
    @api.constrains('estado', 'asistentes_reales')
    def _check_asistentes_finalizada(self):
        for record in self:
            if record.estado == 'finalizada' and record.asistentes_reales is None:
                raise ValidationError('Debe indicar el número de asistentes reales si la sesión ha finalizado')