# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_cita(models.Model):

    _name = 'rrhh_upo.tipo_cita'
    _description = 'Tipo de la cita'

    name = fields.Char(string='Nombre',required=True,  size = 20,help='Rellene el nombre del tipo de cita')
    sDescripcion = fields.Text('Descripcion',size = 240)
    fDuracion_estimada = fields.Float('Duración estimada (h)', default = 0.6)
    bReagendable = fields.Boolean('Reagendable', default =True)
    iMargen_antelacion = fields.Integer('Margen de antelacion (días)', default = 1)
    sFormato = fields.Selection([
        ('telematico','Telemático'),
        ('presencial','Presencial'),
        ('mixto','Mixto'),
    ],'Formato')

    #cita_id = fields.One2many('rrhh_upo.cita',string='Cita')

    #No dura menos o 0 horas
    @api.constrains('fDuracion_estimada')
    def _check_duracion_estimada(self):
        for record in self:
            if record.fDuracion_estimada <= 0:
                raise ValidationError('La duración estimada debe ser un valor positivo')

    #Margen no menos de 0 días
    @api.constrains('iMargen_antelacion')
    def _check_margen_antelacion(self):
        for record in self:
            if record.iMargen_antelacion < 0:
                raise ValidationError('El margen de antelación no puede ser negativo')

    _sql_constraints = [('tipo_cita_unico', 'unique(name)', 'El nombre debe ser unico')]