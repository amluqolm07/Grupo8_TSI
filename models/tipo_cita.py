# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tipo_cita(models.Model):

    _name = 'rrhh_upo.tipo_cita'
    _description = 'Tipo de la cita'

    name = fields.Char(string='Nombre',required=True,  size = 20,elp='Rellene el nombre del tipo de cita')
    descripcion = fields.Text('Descripcion',size = 240)
    duracion_estimada = fields.Float('Duración estimada (h)', default = 0.6)
    reagendable = fields.Boolean('Reagendable', default =True)
    margen_antelacion = fields.Integer('Margen de antelacion (días)', default = 1)
    formato = fields.Selection([
        ('telematico','Telemático'),
        ('presencial','Presencial'),
        ('mixto','Mixto'),
    ],'Formato')