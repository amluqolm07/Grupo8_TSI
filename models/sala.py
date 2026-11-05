# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sala(models.Model):

    _name = 'rrhh_upo.sala'
    _description = 'Sala'
    _rec_name = 'numero'

    numero = fields.Integer(string='Número',required=True,help='Rellene el número de la sala')
    planta = fields.Integer('Planta') #Restricciones numéricas?

    aforo = fields.Integer('Aforo')
    superficie = fields.Float('Superficie (m^2)')
    altura = fields.Float('Altura (m)')
    hora_apertura = fields.Float('Hora de apertura')
    hora_cierre = fields.Float('Hora de cierre')
    estado = fields.Selection([
        ('disponible','Disponible'),
        ('ocupada','Ocupada'),
        ('mantenimiento','Mantenimiento'),
    ],'Estado')

    dimensiones = fields.Float('Dimensiones (m^3)',compute='calcular_dimensiones')

    #Dimensiones = superficie * altura
    @api.depends('superficie','altura')
    def calcular_dimensiones(self):
        for record in self:
            if record.superficie and record.altura:
                record.dimensiones = record.superficie * record.altura
            else:
                record.dimensiones = 0.0

    #Valores numéricos mayores a 0
    @api.constrains('superficie', 'altura', 'aforo')
    def _check_valores_positivos(self):
        for record in self:
            if record.superficie and record.superficie <= 0:
                raise ValidationError('La superficie debe ser un valor positivo')
            if record.altura and record.altura <= 0:
                raise ValidationError('La altura debe ser un valor positivo')
            if record.aforo and record.aforo <= 0:
                raise ValidationError('El aforo debe ser mayor que cero')

    #Comprobación de las hroas
    @api.constrains('hora_apertura', 'hora_cierre')
    def _check_horas_operativas(self):
        for record in self:
            if record.hora_apertura and (record.hora_apertura < 0 or record.hora_apertura > 24):
                raise ValidationError('La hora de apertura debe estar entre 0 y 24')
            if record.hora_cierre and (record.hora_cierre < 0 or record.hora_cierre > 24):
                raise ValidationError('La hora de cierre debe estar entre 0 y 24')