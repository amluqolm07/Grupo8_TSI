# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_sesion(models.Model):

    _name = 'rrhh_upo.tipo_sesion'
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

    #Aforo mayor igual a 0
    @api.constrains('aforo_recomendado')
    def _check_aforo_recomendado(self):
        for record in self:
            if record.aforo_recomendado and record.aforo_recomendado <= 0:
                raise ValidationError('El aforo recomendado debe ser un valor positivo')