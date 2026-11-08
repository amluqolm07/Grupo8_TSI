# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_entrevista(models.Model):

    _name = 'rrhh_upo.tipo_entrevista'
    _description = 'Tipo de la entrevista'

    name = fields.Char(string='Nombre',required=True,  size = 20,elp='Rellene el nombre del tipo de la entrevista')
    sDescripcion = fields.Text('Descripcion',size = 240)
    fDuracion_estimada = fields.Float('Duración estimada (h)', default = 0.6)
    iPersonal_necesario = fields.Integer('Personal necesario', help='Personal de la UPO que debe acudir a realizar la cita')
    sModalidad = fields.Selection([
           ('estructurada','Estructurada'),
           ('no estructurada','No estructurada'),
           ('semiestructurada','Semiestructurada'),
           ('por competencias','Por competencias'),
        ],'Modalidad')
    sFormato = fields.Selection([
        ('telematico','Telemático'),
        ('presencial','Presencial'),
    ],'Formato')


    #entrevista_id = fields.One2many('rrhh_upo.entrevista',string='Entrevista')

    #Duración no menor igual a 0
    @api.constrains('fDuracion_estimada')
    def _check_duracion_estimada(self):
        for record in self:
            if record.fDuracion_estimada <= 0:
                raise ValidationError('La duración estimada debe ser un valor positivo')

    #Personal no menor igual a 0
    @api.constrains('iPersonal_necesario')
    def _check_personal_necesario(self):
        for record in self:
            if record.iPersonal_necesario and record.iPersonal_necesario <= 0:
                raise ValidationError('Hace falta algún personal')

    _sql_constraints = [('Tipo_entrevista_unico', 'unique(name)', 'El nombre debe ser unico')]        