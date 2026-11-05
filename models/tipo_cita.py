# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_cita(models.Model):

    _name = 'rrhh_upo.tipo_cita'
    _description = 'Tipo de la cita'

    name = fields.Char(string='Nombre',required=True,  size = 20,help='Rellene el nombre del tipo de cita')
    descripcion = fields.Text('Descripcion',size = 240)
    duracion_estimada = fields.Float('Duración estimada (h)', default = 0.6)
    reagendable = fields.Boolean('Reagendable', default =True)
    margen_antelacion = fields.Integer('Margen de antelacion (días)', default = 1)
    formato = fields.Selection([
        ('telematico','Telemático'),
        ('presencial','Presencial'),
        ('mixto','Mixto'),
    ],'Formato')

    #No dura menos o 0 horas
    @api.constrains('duracion_estimada')
    def _check_duracion_estimada(self):
        for record in self:
            if record.duracion_estimada <= 0:
                raise ValidationError('La duración estimada debe ser un valor positivo')

    #Margen no menos de 0 días
    @api.constrains('margen_antelacion')
    def _check_margen_antelacion(self):
        for record in self:
            if record.margen_antelacion < 0:
                raise ValidationError('El margen de antelación no puede ser negativo')