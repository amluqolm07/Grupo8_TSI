# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Jornada(models.Model):
    _name='rrhh_upo.jornada'
    _description = 'Jornada'


    sTipo = fields.Selection([
        ('completa', 'Completa'),
        ('parcial', 'Parcial')
    ],string='Tipo de jornada',required=True)
    sObservaciones = fields.text()
    fHorasDiarias = fields.Float(string='Horas diarias',required=True,help='Introduce el número de horas diarias de la jornada')

    oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo','Oferta de empleo',required=True)
    horario_ids = fields.One2many('rrhh_upo.horario','Horario')

    #PREGUNTA AURELIO: meto oferta_id dentro del unique??
    _sql_constraints = [('jornada_unica', 'UNIQUE(sTipo)','Una oferta de empleo solo puede tener una jornada')]