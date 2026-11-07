# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_sesion(models.Model):

    _name = 'rrhh_upo.tipo_sesion'
    _description = 'Tipo de la sesion'

    name = fields.Char(string='Nombre',required=True,size = 20, help='Rellene el nombre del tipo de sesion')
    sDescripcion = fields.Text('Descripción',size = 240)
    bAsistencia_obligatoria = fields.Boolean('Obligatorio asistir', default=True)
    iAforo_recomendado = fields.Integer('Aforo recomendado')
    sModalidad = fields.Selection([
        ('presencial','Presencial'),
        ('telematica','Telemática'),
        ('mixta','Mixta'),
    ],'Modalidad')

    sesion_id=fields.One2many('rrhh_upo.sesion',string='Sesion')

    #Aforo mayor igual a 0
    @api.constrains('iAforo_recomendado')
    def _check_aforo_recomendado(self):
        for record in self:
            if record.iAforo_recomendado and record.iAforo_recomendado <= 0:
                raise ValidationError('El aforo recomendado debe ser un valor positivo')

    _sql_constraints = [('Tipo_sesion_unico', 'unique(name)', 'El nombre debe ser unico')]