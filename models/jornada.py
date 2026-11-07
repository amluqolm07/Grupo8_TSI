# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Jornada(models.Model):
    _name='rrhh_upo.jornada'
    _description = 'Jornada'
    _rec_name = 'name'

    #Autocalcualdo
    name = fields.Char(string='Nombre de la jornada', compute='generador_nombre_jornada',store=True)
    sTipo = fields.Selection([
        ('completa', 'Completa'),
        ('parcial', 'Parcial')
    ],string='Tipo de jornada',required=True)
    sObservaciones = fields.Text()
    fHorasDiarias = fields.Float(string='Horas diarias',required=True,help='Introduce el número de horas diarias de la jornada')

    oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo','Oferta de empleo',required=True)
    horario_ids = fields.One2many('rrhh_upo.horario','jornada_id','Horario')

    
    _sql_constraints = [('jornada_unica', 'UNIQUE(name)','Una oferta de empleo solo puede tener una jornada')]

    #Genero el name combinando el tipo y el name de oferta de empleo
    @api.depends('sTipo', 'oferta_empleo_id.name')
    def generador_nombre_jornada(self):
        for record in self:
            if record.sTipo and record.oferta_empleo_id:
                tipo = dict(record._fields['sTipo'].selection).get(record.sTipo)
                record.name = f'{tipo} - {record.oferta_empleo_id.name}'
            else:
                record.name = False

    @api.constrains('fHorasDiarias')
    def validar_horas(self):
        for record in self:
            if record.fHorasDiarias <= 0:
                raise models.ValidationError('Las horas diarias deben ser mayores que 0')

    