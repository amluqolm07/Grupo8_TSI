# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Sesion(models.Model):

    _name = 'rrhh_upo.sesion'
    _description = 'Sesion'
  
    name = fields.Char(string='id', size=7, required=True, help='Rellene el id de la sesion (7 carácteres)')
    dFecha_hora_inicio = fields.Datetime('Fecha y hora de inicio')
    fDuracion = fields.Float(string='Duración (h)', default = 1)
    sIncidencias = fields.Text("Incidencias",size = 240)
    iAsistentes_previstos = fields.Integer("Asistentes previstos")
    iAsistentes_reales = fields.Integer("Asistentes reales")
    bGrabada = fields.Boolean('Sesion grabada', default=False)
    sEstado = fields.Selection([
            ('pendiente','Pendiente'),
            ('finalizada','Finalizada'),
            ('cancelada','Cancelada'),
        ],'Estado')

    dFecha_hora_final = fields.Datetime('Fecha y hora en la que acaba la sesion', compute='_calcular_fecha_hora_final', stored=True)

    sala_id = fields.Many2one('rrhh_upo.sala',string='Sala')
    #pdi_id = fields.Many2one('rrhh_upo.pdi',string='PDI')
    #asignatura_id = fields.Many2one('rrhh_upo.asignatura',string='Asignatura')
    #alumno_ids = fields.Many2many('rrhh_upo.alumno',string='Alumno')
    #tipo_sesion_id = fields.Many2one('rrhh_upo.tipo_sesion',string='Tipo de la sesion')

    #Final = inicio + duración
    @api.depends('dFecha_hora_inicio','fDuracion')
    def _calcular_fecha_hora_final(self):
        for record in self:
            if record.fDuracion and record.dFecha_hora_inicio:
                record.dFecha_hora_final = record.dFecha_hora_inicio + timedelta(hours=record.fDuracion)
            else:
                record.dFecha_hora_final = False

    #No puede durar menos de 0 horas
    @api.constrains('fDuracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.fDuracion <= 0:
                raise ValidationError('La duración de la sesión debe ser un valor positivo')

    #Ninguna asistencia menor a 0
    @api.constrains('iAsistentes_previstos', 'iAsistentes_reales')
    def _check_asistentes(self):
        for record in self:
            if record.iAsistentes_previstos and record.iAsistentes_previstos < 0:
                raise ValidationError('Los asistentes previstos no pueden ser negativos')
            if record.iAsistentes_reales and record.iAsistentes_reales < 0:
                raise ValidationError('Los asistentes reales no pueden ser negativos')

    #No puede terminar sin saber cuantos han ido
    @api.constrains('sEstado', 'iAsistentes_reales')
    def _check_asistentes_finalizada(self):
        for record in self:
            if record.sEstado == 'finalizada' and record.iAsistentes_reales is None:
                raise ValidationError('Debe indicar el número de asistentes reales si la sesión ha finalizado')
    '''
    # No coinciden en la misma sala en el mismo intervalo de tiempo entrevista, cita o sesión
    @api.constrains('sala_id', 'dFecha_hora_inicio', 'dFecha_hora_final')
    def _check_solapamiento_sala(self):
        for record in self:
            if record.sala_id and record.dFecha_hora_inicio and record.dFecha_hora_final:
                sesiones_existentes = self.search([
                    ('sala_id', '=', record.sala_id.id),
                    ('id', '!=', record.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_final),
                    ('dFecha_hora_final', '>', record.dFecha_hora_inicio),
                ])
                citas_existentes = self.env['rrhh_upo.cita'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_cita', '<', record.dFecha_hora_final),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_inicio),
                ])
                entrevistas_existentes = self.env['rrhh_upo.entrevista'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_final),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_inicio),
                ])

                if sesiones_existentes or citas_existentes or entrevistas_existentes:
                    raise ValidationError('La sala ya esta ocupada en ese intervalo de tiempo')
    '''

    _sql_constraints = [('Sesion_unica', 'unique(name)', 'El id de la sesion debe ser unico')]