# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Cita(models.Model):

    _name = 'rrhh_upo.cita'
    _description = 'Cita'

    name = fields.Char(string='id', size=7,required=True, help='Rellene el id de la cita (7 carácteres)')
    duracion = fields.Float('Duración (h)', default = 0.5)
    motivo = fields.Text('Motivo',size = 120, required = True)
    fecha_hora_cita = fields.Datetime('Fecha y hora de la cita')
    medio_concertada = fields.Selection([
        ('email','Email'),
        ('telefono','Teléfono'),
        ('presencial','Presencial'),
    ],'Medio concertada')
    fecha_hora_agendada = fields.Datetime('Fecha y hora agendada')
    estado = fields.Selection([
            ('pendiente','Pendiente'),
            ('finalizada','Finalizada'),
            ('cancelada','Cancelada'),
        ],'Estado')
    conclusion = fields.Text('Conclusión')

    fecha_hora_fin = fields.Datetime(string='Fecha y hora fin', compute='calcular_fecha_hora_fin')

    empleado_ids = fields.Many2many('rrhh_upo.empleado', string='Empleado') #enganche con empleado
    tipo_cita_id = fields.Many2one('rrhh_upo.tipo_cita', string='Tipo de la cita')
    sala_id = fields.Many2one('rrhh_upo.sala', string='Sala')

    #Final = inicio + duración
    @api.depends('fecha_hora_cita', 'duracion')
    def calcular_fecha_hora_fin(self):
        for record in self:
            if record.fecha_hora_cita and record.duracion:
                record.fecha_hora_fin = record.fecha_hora_cita + timedelta(hours=record.duracion)
            else:
                record.fecha_hora_fin = False

    #La cita necesita de mínimo dos empleados
    @api.constrains('empleado_ids')
    def _check_numero_empleados(self):
        for record in self:
            if len(record.empleado_ids) < 2:
                raise ValidationError('Una cita debe contar con al menos 2 empleados asignados')

    #No se empieza antes de reservarse
    @api.constrains('fecha_hora_cita', 'fecha_hora_agendada')
    def _check_fechas_coherencia(self):
        for record in self:
            if record.fecha_hora_agendada and record.fecha_hora_cita and record.fecha_hora_agendada > record.fecha_hora_cita:
                raise ValidationError('La fecha y hora agendada no puede ser posterior a la fecha y hora de la cita')

    #No puede durar menos de 0 horas
    @api.constrains('duracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.duracion <= 0:
                raise ValidationError('La duración de la cita debe ser mayor que cero')

    #No puede estar finalizada y no tener conclusión
    @api.constrains('estado', 'conclusion')
    def _check_conclusion_finalizada(self):
        for record in self:
            if record.estado == 'finalizada' and not record.conclusion:
                raise ValidationError('Debe rellenar la conclusión si la cita está finalizada')
    