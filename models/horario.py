# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Horario(models.Model):
    _name='rrhh_upo.horario'
    _description = 'Horario'
    _rec_name = 'name'

    #Autocalculado
    name = fields.Char(string='Nombre de la jornada', compute='generador_nombre_horario',store=True)
    sTurno = fields.Selection([
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche')
    ],string='Turno',required=True)
    fHoraInicio = fields.Float(string='Hora de inicio',required=True, help='Introduce la hora de inicio')
    fHoraFin = fields.Float(string='Hora de finalización',required=True, help='Introduce la hora de finalización')


    jornada_id = fields.Many2one('rrhh_upo.jornada','Jornada',required=True)


    _sql_constraints = [('horario_unico', 'UNIQUE(name)','Ya existe un horario con esa hora de inicio para esta jornada')]

    #Genero nombre para horario combinando la hora de inicio con el name de jornada que ya se combina con oferta de empleo
    @api.depends('fHoraInicio', 'jornada_id.name')
    def generador_nombre_horario(self):
        for record in self:
            if record.jornada_id:
                record.name = f'{record.fHoraInicio} - {record.jornada_id.name}'
            else:
                record.name = False
    
    @api.constrains('fHoraInicio', 'fHoraFin')
    def validar_horas(self):
        for record in self:
            if record.fHoraInicio < 0 or record.fHoraInicio >= 24:
                raise models.ValidationError('La hora de inicio debe estar entre 0 y 24')

            if record.fHoraFin <= 0 or record.fHoraFin > 24:
                raise models.ValidationError('La hora de finalización debe estar entre 0 y 24')

            if record.fHoraFin <= record.fHoraInicio:
                 raise models.ValidationError('La hora de finalización debe ser posterior a la de inicio')