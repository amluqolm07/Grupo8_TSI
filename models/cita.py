# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cita(models.Model):

    _name = 'rrhh.upo.cita'
    _description = 'Cita'

    name = fields.Char(string='id', size=7,required=True, help='Rellene el id de la cita (7 carácteres)')
    duracion = fields.Float('Duración (h)', default = 0.5)
    motivo = fields.Text('Motivo',required = True)
    fecha_hora_cita = fields.Datetime('Fecha y hora de la cita')
    medio_concertada = fieds.Selection([
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