# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Historial_laboral(models.Model):
    _name = 'rrhh_upo.historial.laboral'
    _description = 'Historial laboral'
    _rec_name = 'fecha_inicio'

    fecha_inicio = fields.Date(name='Fecha de inicio',required=True,help='Fecha en la que inició en el puesto')
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

    dias_en_puesto = fields.Integer('Días en el puesto', compute = 'calcular_dias_en_puesto')

    #Días trabajados = fin - inicio
    @api.depends('fecha_inicio','fecha_fin')
    def calcular_dias_en_puesto(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                record.dias_en_puesto = (record.fecha_fin - record.fecha_inicio).days
            else:
                record.dias_en_puesto = 0

    #No puede acabar antes de empezar el puesto
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_historial(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio')

    #No puede haber cobrado negativo
    @api.constrains('sueldo')
    def _check_sueldo_positivo(self):
        for record in self:
            if record.sueldo is not None and record.sueldo <= 0:
                raise ValidationError('El sueldo debe ser un valor positivo mayor que cero')

    #Si ha terminado debe especificarse porqué
    @api.constrains('fecha_fin', 'motivo_cambio')
    def _check_motivo_cambio_requerido(self):
        for record in self:
            if record.fecha_fin and not record.motivo_cambio:
                raise ValidationError('Debe especificar el motivo del cambio si se ha indicado una fecha final en el puesto')