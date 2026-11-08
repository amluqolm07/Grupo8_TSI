# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_sala(models.Model):

    _name = 'rrhh_upo.tipo_sala'
    _description = 'Tipo de la sala'

    name = fields.Char(string='Nombre',required=True, size = 20, help='Rellene el nombre del tipo de sala')
    sNormativa = fields.Text('Normativa',size = 240)
    bAcceso_internet = fields.Boolean('Acceso a internet', default=False)
    bDigitalizada = fields.Boolean('Digitalizada', default=False)
    bClimatizada = fields.Boolean('Climatizada', default=False)
    bAdaptada = fields.Boolean('Adaptada', default=False)

    #sala_id = fields.One2many('rrhh_upo.sala',string='Sala')

    _sql_constraints = [('Tipo_sala_unico', 'unique(name)', 'El nombre debe ser unico')]