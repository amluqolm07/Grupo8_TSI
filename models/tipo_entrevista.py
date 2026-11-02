# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tipo_entrevista(models.Model):

    _name = 'rrhh.upo.tipo.entrevista'
    _description = 'Tipo de la entrevista'

    name = fields.Char(string='Nombre',required=True,  size = 20,elp='Rellene el nombre del tipo de la entrevista')
    descripcion = fields.Text('Descripcion',size = 240)
    duracion_estimada = fields.Float('Duración estimada (h)', default = 0.6)
    personal_necesario = fields.Integer('Personal necesario', help='Personal de la UPO que debe acudir a realizar la cita')
    modalidad = fields.Selection([
           ('estructurada','Estructurada'),
           ('no estructurada','No estructurada'),
           ('semiestructurada','Semiestructurada'),
           ('por competencias','Por competencias'),
       ],'Modalidad')
    formato = fields.Selection([
        ('telematico','Telemático'),
        ('presencial','Presencial'),
    ],'Formato')