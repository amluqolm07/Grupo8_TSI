# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError

class TipoConcepto(models.Model):
    _name = 'rrhh_upo.tipo_concepto'
    _description = 'Tipo de concepto'
    _rec_name = 'sNombre'

    sCodigo = fields.Char(string='Código', size=10,required=True, help = 'Introduce el código para identificar el concepto')
    #Número decimal entre 0 y 100. Por defecto viene en 0
    fPorcentaje = fields.Float(string='Porcentaje', digits=(5, 2), default=0.0)
    sNombre = fields.Char(string='Nombre', size=30, required=True, help = 'Introduce el nombre del concepto')
    sDescripcion = fields.Text()
    #True = deducción (resta) y False = no es deducción (suma). Por defecto False
    bEsDeduccion = fields.Boolean(string='Es deducción', default=False)
    

    #Validación: Valido tanto que no este en blanco el código
    @api.constrains('sCodigo')
    def validar_codigo(self):
        for record in self:
            codigo = record.sCodigo.strip()
            if not codigo:
                raise ValidationError('El código no puede estar en blanco')
            

    #Validación: Valido tanto que no este en blanco el nombre
    @api.constrains('sNombre')
    def validar_nombre(self):
        for record in self:
            nombre = record.sNombre.strip()
            if not nombre:
                raise ValidationError('El nombre no puede estar en blanco')
            
            
    #Validación: El porcentaje debe estar entre 0 y 100
    @api.constrains('fPorcentaje')
    def validar_porcentaje(self):
        for record in self:
            if not 0 <= record.fPorcentaje <= 100:
                raise ValidationError('El porcentaje debe estar entre 0 y 100')


    concepto_ids = fields.One2many('rrhh_upo.concepto','Concepto')

    _sql_constraints = [('codigo_unico', 'UNIQUE ("sCodigo")', 'Ya existe un tipo de concepto con ese código')]