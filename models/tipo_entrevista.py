# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_entrevista(models.Model):

    _name = 'rrhh_upo.tipo_entrevista'
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

    #Duración no menor igual a 0
    @api.constrains('duracion_estimada')
    def _check_duracion_estimada(self):
        for record in self:
            if record.duracion_estimada <= 0:
                raise ValidationError('La duración estimada debe ser un valor positivo')

    #Personal no menor igual a 0
    @api.constrains('personal_necesario')
    def _check_personal_necesario(self):
        for record in self:
            if record.personal_necesario and record.personal_necesario <= 0:
                raise ValidationError('Hace falta algún personal')