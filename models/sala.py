# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sala(models.Model):

    _name = 'rrhh_upo.sala'
    _description = 'Sala'

    name = fields.Char(string='id', size=7, required=True, help='Rellene el id de la sala (7 carácteres)')
    iNumero = fields.Integer('Número')
    iPlanta = fields.Integer('Planta') 
    iAforo = fields.Integer('Aforo')
    fSuperficie = fields.Float('Superficie (m^2)')
    fAltura = fields.Float('Altura (m)')
    fHora_apertura = fields.Float('Hora de apertura')
    fHora_cierre = fields.Float('Hora de cierre')
    sEstado = fields.Selection([
        ('disponible','Disponible'),
        ('ocupada','Ocupada'),
        ('mantenimiento','Mantenimiento'),
    ],'Estado')

    fDimensiones = fields.Float('Dimensiones (m^3)',compute='_calcular_dimensiones', stored=True)

    cita_id = fields.One2many('rrhh_upo.cita',string='Cita')
    entrevista_id = fields.One2many('rrhh_upo.cita',string='Entrevista')
    tipo_sala_id = fields.Many2one('rrhh_upo.tipo_sala',string='Tipo sala')
    edificio_id = fields.Many2one('rrhh_upo.edificio',string='Edificio')
    sesion_id = fields.One2many('rrhh_upo.sesion',string='Sesion')



    #Dimensiones = superficie * altura
    @api.depends('fSuperficie','fAltura')
    def _calcular_dimensiones(self):
        for record in self:
            if record.fSuperficie and record.fAltura:
                record.fDimensiones = record.fSuperficie * record.fAltura
            else:
                record.fDimensiones = 0.0

    #Valores numéricos mayores a 0
    @api.constrains('fSuperficie', 'fAltura', 'iAforo')
    def _check_valores_positivos(self):
        for record in self:
            if record.fSuperficie and record.fSuperficie <= 0:
                raise ValidationError('La superficie debe ser un valor positivo')
            if record.fAltura and record.fAltura <= 0:
                raise ValidationError('La altura debe ser un valor positivo')
            if record.iAforo and record.iAforo <= 0:
                raise ValidationError('El aforo debe ser mayor que cero')

    #Comprobación de las hroas
    @api.constrains('fHora_apertura', 'fHora_cierre')
    def _check_horas_operativas(self):
        for record in self:
            if record.fHora_apertura and (record.fHora_apertura < 0 or record.fHora_apertura > 24):
                raise ValidationError('La hora de apertura debe estar entre 0 y 24')
            if record.fHora_cierre and (record.fHora_cierre < 0 or record.fHora_cierre > 24):
                raise ValidationError('La hora de cierre debe estar entre 0 y 24')

    #Dirección de la sala única
    _sql_constraints = [('Sala_unica', 'unique(name)', 'El id de la sala debe ser unico'),
                        ('Dirección_unica', 'unique(iNumero, iPlanta, edificio_id)', 'Ya existe una sala con esa dirección exacta')]