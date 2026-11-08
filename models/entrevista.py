# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Entrevista(models.Model):

    _name = 'rrhh_upo.entrevista'
    _description = 'Entrevista'


    name = fields.Char(string='id', size=7, required=True, help='Rellene el id de la entrevista (7 carácteres)')
    dFecha_hora_inicio = fields.Datetime('Fecha y hora de inicio')
    fDuracion = fields.Float(string='Duración (h)', default = 0.6)
    sInformación_previa = fields.Text("Información previa", size = 400)
    sApuntes = fields.Text("Apuntes post-entrevista", size = 400)
    dFecha_hora_agendada = fields.Datetime('Fecha y hora agendada')
    sResultado = fields.Selection([
        ('muy favorable','Muy favorable'),
        ('favorable','Favorable'),
        ('aceptable','Aceptable'),
        ('no aceptable','No aceptable'),
        ('pendiente','Pendiente'),
    ],'Resultado')

    dFecha_hora_fin = fields.Datetime('Fecha y hora fin', compute='_calcular_fecha_hora_fin', stored=True)

    #Problemas para arrancar el odoo
    #personal_tecnico_ids = fields.Many2many('rrhh_upo.personal_tecnico',string='Personal técnico')
    #empleado_rrhh_ids = fields.Many2many('rrhh_upo.empleado_rrhh',string='Empleado de recursos humanos')
    #empleado_externo_ids = fields.Many2many('rrhh_upo.empleado_externo',string='Empleado externo')
    
    #sala_id = fields.Many2one('rrhh_upo.sala', string='Sala')
    #solicitud_id = fields.Many2one('rrhh_upo.solicitud', string='Solicitud de empleo')
    #tipo_entrevista_id = fields.Many2one('rrhh_upo.tipo_entrevista',string='Tipo de la entrevista')

    #Final = inicio + duración
    @api.depends('dFecha_hora_inicio', 'fDuracion')
    def _calcular_fecha_hora_fin(self):
        for record in self:
            if record.dFecha_hora_inicio and record.fDuracion:
                record.dFecha_hora_fin = record.dFecha_hora_inicio + timedelta(hours=record.fDuracion)
            else:
                record.dFecha_hora_fin = False

    #No puede durar menos de 0 horas
    @api.constrains('fDuracion')
    def _check_duracion_positiva(self):
        for record in self:
            if record.fDuracion <= 0:
                raise ValidationError('La duración de la entrevista debe ser un valor positivo')

    #No puede empezar antes de ser agendada
    @api.constrains('dFecha_hora_inicio', 'dFecha_hora_agendada')
    def _check_fechas_coherencia(self):
        for record in self:
            if record.dFecha_hora_agendada and record.dFecha_hora_inicio and record.dFecha_hora_agendada > record.dFecha_hora_inicio:
                raise ValidationError('La fecha en la que se agendó no puede ser posterior a la fecha de inicio de la entrevista')

    #Debe incluir apuntes si ya está evaluado
    @api.constrains('sResultado', 'sApuntes')
    def _check_apuntes_si_realizada(self):
        for record in self:
            if record.sResultado and record.sResultado != 'pendiente' and not record.sApuntes:
                raise ValidationError('Debe incluir apuntes si ya se ha obtenido resultado')

    '''
    # No coinciden en la misma sala en el mismo intervalo de tiempo entrevista, cita o sesión
    @api.constrains('sala_id', 'dFecha_hora_inicio', 'dFecha_hora_fin')
    def _check_solapamiento_sala(self):
        for record in self:
            if record.sala_id and record.dFecha_hora_inicio and record.dFecha_hora_fin:
                entrevistas_existentes = self.search([
                    ('sala_id', '=', record.sala_id.id),
                    ('id', '!=', record.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_inicio),
                ])
                citas_existentes = self.env['rrhh_upo.cita'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_cita', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_fin', '>', record.dFecha_hora_inicio),
                ])
                sesiones_existentes = self.env['rrhh_upo.sesion'].search([
                    ('sala_id', '=', record.sala_id.id),
                    ('dFecha_hora_inicio', '<', record.dFecha_hora_fin),
                    ('dFecha_hora_final', '>', record.dFecha_hora_inicio),
                ])

                if entrevistas_existentes or citas_existentes or sesiones_existentes:
                    raise ValidationError('La sala ya esta ocupada en ese intervalo de tiempo')
    '''
    _sql_constraints = [('Entrevista_unica', 'unique(name)', 'El id de la entrevista debe ser unico')]