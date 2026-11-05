# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Entrevista(models.Model):

    _name = 'rrhh_upo.entrevista'
    _description = 'Entrevista'
    _rec_name = 'fecha_hora_inicio'


    fecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio',required=True, help='Rellene su fecha y hora de inicio')
    duracion = fields.Float(string='Duración (h)', default = 0.6)
    información_previa = fields.Text("Información previa", size = 400)
    apuntes = fields.Text("Apuntes post-entrevista", size = 400)
    fecha_hora_agendada = fields.Datetime('Fecha y hora agendada')
    resultado = fields.Selection([
        ('muy favorable','Muy favorable'),
        ('favorable','Favorable'),
        ('aceptable','Aceptable'),
        ('no aceptable','No aceptable'),
        ('pendiente','Pendiente'),
    ],'Resultado')

    fecha_hora_fin = fields.Datetime('Fecha y hora fin', compute='calcular_fecha_hora_fin')
    
    sala_id = fields.Many2one('rrhh.upo.sala', string='Sala')
    empleado_rrhh = fields.Many2one('rrhh_upo.empleado_rrhh', string='Empleado de RRHH')

    #Final = inicio + duración
    @api.depends('fecha_hora_inicio', 'duracion')
    def calcular_fecha_hora_fin(self):
        for record in self:
            if record.fecha_hora_inicio and record.duracion:
                record.fecha_hora_fin = record.fecha_hora_inicio + timedelta(hours=record.duracion)
            else:
                record.fecha_hora_fin = False

    #No puede durar menos de 0 horas
    @api.constrains('duracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.duracion <= 0:
                raise ValidationError('La duración de la entrevista debe ser un valor positivo')

    #No puede empezar antes de ser agendada
    @api.constrains('fecha_hora_inicio', 'fecha_hora_agendada')
    def _check_fechas_coherencia(self):
        for record in self:
            if record.fecha_hora_agendada and record.fecha_hora_inicio and record.fecha_hora_agendada > record.fecha_hora_inicio:
                raise ValidationError('La fecha en la que se agendó no puede ser posterior a la fecha de inicio de la entrevista')

    #No puede no incluir apuntes si ya está evaluado
    @api.constrains('resultado', 'apuntes')
    def _check_apuntes_si_realizada(self):
        for record in self:
            if record.resultado and record.resultado != 'pendiente' and not record.apuntes:
                raise ValidationError('Debe incluir apuntes si ya se ha obtenido resultado')