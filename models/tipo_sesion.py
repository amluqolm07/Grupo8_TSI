# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tipo_sesion(models.Model):

    _name = 'rrhh.upo.tipo.sesion'
    _description = 'Tipo de la sesion'

    name = fields.Char(string='Nombre',required=True,size = 20, help='Rellene el nombre del tipo de sesion')
    descripcion = fields.Text('Descripción',size = 240)
    asistencia_obligatoria = fields.Boolean('Obligatorio asistir', default=True)
    aforo_recomendado = fields.Integer('Aforo recomendado')
    modalidad = fields.Selection([
        ('presencial','Presencial'),
        ('telematica','Telemática'),
        ('mixta','Mixta'),
    ],'Modalidad')