# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Historial_laboral(models.Model):
    _name = 'rrhh_upo.historial_laboral'
    _description = 'Historial laboral'
   
    name = fields.Char(string='id', size=7, required=True, help='Rellene el id del historial laboral (7 carácteres)')
    dFecha_inicio = fields.Date('Fecha de inicio')
    sPuesto = fields.Selection([
        ('personal tecnico', 'Personal Técnico'),
        ('pdi', 'PDI'),
        ('empleado externo', 'Empleado Externo'),
        ('rrhh', 'RRHH'),
    ], 'Puesto')

    sRol = fields.Char('Rol') # -*- PENDIENTE

    fSueldo = fields.Float('Sueldo')
    dFecha_fin = fields.Date('Fecha final')
    sMotivo_cambio = fields.Text('Motivo del cambio', size=240)

    iDias_en_puesto = fields.Integer('Días en el puesto', compute='_calcular_dias_en_puesto', stored=True)

    #empleado_id = fields.Many2one('rrhh_upo.empleado',string='Empleado')

    # Días trabajados = fin - inicio
    @api.depends('dFecha_inicio', 'dFecha_fin')
    def _calcular_dias_en_puesto(self):
        for record in self:
            if record.dFecha_inicio and record.dFecha_fin:
                record.iDias_en_puesto = (record.dFecha_fin - record.dFecha_inicio).days
            else:
                record.iDias_en_puesto = 0

    # No puede acabar antes de empezar el puesto
    @api.constrains('dFecha_inicio', 'dFecha_fin')
    def _check_fechas_historial(self):
        for record in self:
            if record.dFecha_fin and record.dFecha_inicio and record.dFecha_fin < record.dFecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio')

    # No puede haber cobrado negativo
    @api.constrains('fSueldo')
    def _check_sueldo_positivo(self):
        for record in self:
            if record.fSueldo is not None and record.fSueldo <= 0:
                raise ValidationError('El sueldo debe ser un valor positivo mayor que cero')

    # Si ha terminado debe especificarse porqué
    @api.constrains('dFecha_fin', 'sMotivo_cambio')
    def _check_motivo_cambio_requerido(self):
        for record in self:
            if record.dFecha_fin and not record.sMotivo_cambio:
                raise ValidationError('Debe especificar el motivo del cambio si se ha indicado una fecha final en el puesto')

        _sql_constraints = [('Historial_laboral_unico', 'unique(name)', 'El id del historial laboral debe ser unico')]