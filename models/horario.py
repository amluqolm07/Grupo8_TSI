# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Horario(models.Model):
    _name='rrhh_upo.horario'
    _description = 'Horario'

    sTurno = fields.Selection([
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche')
    ],string='Turno',required=True)
    fHoraInicio = fields.Float(string='Hora de inicio',required=True, help='Introduce la hora de inicio')
    fHoraFin = fields.Float(string='Hora de finalización',required=True, help='Introduce la hora de finalización')





    jornada_id = fields.Many2one('rrhh_upo.jornada','Jornada',required=True)

    #PREGUNTA AURELIO: (referencia_oferta, tipo, hora_inicio) que metro dentro de UNIQUE?
    _sql_constraints = [('horario_unico', 'UNIQUE(fHoraInicio)','Ya existe un horario con esa hora de inicio para esta jornada')]