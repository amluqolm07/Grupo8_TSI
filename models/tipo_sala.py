# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tipo_sala(models.Model):

    _name = 'rrhh.upo.tipo.sala'
    _description = 'Tipo de la sala'

    name = fields.Char(string='Nombre',required=True, size = 20, help='Rellene el nombre del tipo de sala')
    normativa = fields.Text('Normativa',size = 240)
    acceso_internet = fields.Boolean('Acceso a internet', default=False)
    digitalizada = fields.Boolean('Digitalizada', default=False)
    climatizada = fields.Boolean('Climatizada', default=False)
    adaptada = fields.Boolean('Adaptada', default=False)