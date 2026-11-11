# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Cita(models.Model):

    _name = 'rrhh_upo.cita'
    _description = 'Cita'

    name = fields.Char(string='id', size=7, required=True, help='Rellene el id de la cita (7 carácteres)')
    fDuracion = fields.Float('Duración (h)', default=0.5)
    sMotivo = fields.Text('Motivo', size=120, required=True)
    dFecha_hora_cita = fields.Datetime('Fecha y hora de la cita')
    sMedio_concertada = fields.Selection([
        ('email', 'Email'),
        ('telefono', 'Teléfono'),
        ('presencial', 'Presencial'),
    ], 'Medio concertada')
    dFecha_hora_agendada = fields.Datetime('Fecha y hora agendada')
    sEstado = fields.Selection([
            ('pendiente', 'Pendiente'),
            ('finalizada', 'Finalizada'),
            ('cancelada', 'Cancelada'),
        ], 'Estado')
    sConclusion = fields.Text('Conclusión',size=240)

    dFecha_hora_fin = fields.Datetime(string='Fecha y hora fin', compute='_calcular_fecha_hora_fin', stored=True)

    empleado_ids = fields.Many2many('rrhh_upo.empleado', string='Empleado')
    tipo_cita_id = fields.Many2one('rrhh_upo.tipo_cita', string='Tipo de la cita')
    sala_id = fields.Many2one('rrhh_upo.sala', string='Sala')

    _sql_constraints = [('Cita_unica', 'unique(name)', 'El id de la cita debe ser unico')]

    # Final = inicio + duración
    @api.depends('dFecha_hora_cita', 'fDuracion')
    def _calcular_fecha_hora_fin(self):
        for record in self:
            if record.dFecha_hora_cita and record.fDuracion:
                record.dFecha_hora_fin = record.dFecha_hora_cita + timedelta(hours=record.fDuracion)
            else:
                record.dFecha_hora_fin = False

    # La cita necesita de mínimo dos empleados
    @api.constrains('empleado_ids')
    def _check_numero_empleados(self):
        for record in self:
            if len(record.empleado_ids) < 2:
                raise ValidationError('Una cita debe contar con al menos 2 empleados asignados')

    # No se empieza antes de reservarse
    @api.constrains('dFecha_hora_cita', 'dFecha_hora_agendada')
    def _check_fechas_coherencia(self):
        for record in self:
            if record.dFecha_hora_agendada and record.dFecha_hora_cita and record.dFecha_hora_agendada > record.dFecha_hora_cita:
                raise ValidationError('La fecha y hora agendada no puede ser posterior a la fecha y hora de la cita')

    # No puede durar menos de 0 horas
    @api.constrains('fDuracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.fDuracion <= 0:
                raise ValidationError('La duración de la cita debe ser mayor que cero')

    # No puede estar finalizada y no tener conclusión
    @api.constrains('sEstado', 'sConclusion')
    def _check_conclusion_finalizada(self):
        for record in self:
            if record.sEstado == 'finalizada' and not record.sConclusion:
                raise ValidationError('Debe rellenar la conclusión si la cita está finalizada')

    
    # No coinciden en la misma sala en el mismo intervalo de tiempo entrevista, cita o sesión
    @api.constrains('sala_id', 'dFecha_hora_cita', 'dFecha_hora_fin')
    def _check_solapamiento_sala(self):
        for record in self:
            if record.sala_id and record.dFecha_hora_cita and record.dFecha_hora_fin:
                citas_existentes = self.search([
                    ('sala_id', '=', record.sala_id.id),
                    ('id', '!=', record.id),
                    ('dFecha_hora_cita', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_cita),
                ])
                entrevistas_existentes = self.env['rrhh_upo.entrevista'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_cita),
                ])
                sesiones_existentes = self.env['rrhh_upo.sesion'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_final', '>', record.dFecha_hora_cita),
                ])
    
    