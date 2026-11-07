# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoConcepto(models.Model):
    _name = 'rrhh_upo.tipo_concepto'
    _description = 'Tipo de concepto'
    _rec_name = 'name'

    name = fields.Char(string='Código', size=10,required=True, help = 'Introduce el código para identificar el concepto')
    fPorcentaje = fields.Float(string='Porcentaje', default=0.0)
    sNombre = fields.Char(string='Nombre', size=30, required=True, help = 'Introduce el nombre del concepto')
    sDescripcion = fields.Text()
    #True = deducción (resta) y False = no es deducción (suma). Por defecto False
    bEsDeduccion = fields.Boolean(string='Es deducción', default=False)


    concepto_ids = fields.One2many('rrhh_upo.concepto', 'tipo_concepto_id','Conceptos')
    
    _sql_constraints = [('codigo_unico', 'UNIQUE(name)','Ya existe un tipo de concepto con ese código')]

    #Validación: Valido tanto que no este en blanco el código
    @api.constrains('name')
    def validar_codigo(self):
        for record in self:
            if not record.name.strip():
                raise models.ValidationError('El código no puede estar en blanco')
            

    #Validación: Valido tanto que no este en blanco el nombre
    @api.constrains('sNombre')
    def validar_nombre(self):
        for record in self:
            nombre = record.sNombre.strip()
            if not nombre:
                raise models.ValidationError('El nombre no puede estar en blanco')
            
            
    #Validación: El porcentaje debe estar entre 0 y 100
    @api.constrains('fPorcentaje')
    def validar_porcentaje(self):
        for record in self:
            if not 0 <= record.fPorcentaje <= 100:
                raise models.ValidationError('El porcentaje debe estar entre 0 y 100')

    #Aviso al usuario si mete un porcentaje mayor que 0
    @api.onchange('fPorcentaje')
    def onchange_porcentaje(self):
        if self.fPorcentaje > 0:
            return {
            'warning': {'title': 'Tipo porcentual','message': 'Este concepto se calculará mediante porcentaje.'}
        }

    