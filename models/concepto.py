# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError

class Concepto(models.Model):
    _name = 'rrhh_upo.concepto'
    _description = 'Concepto'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string='Nombre', size=30, required=True, help='Escribe un nombre para el concepto')
    sDescripcion = fields.Text()
    #Número decimal con dos decimales. Esto solo se usa si el tipo de concepto no tiene porcentaje. Por defecto va a 0
    fImporteFijo = fields.Float(string='Importe fijo', digits=(10, 2), default=0.0)
    #Autocalculado
    fImporte = fields.Float(string='Importe', digits=(10, 2), compute='calcular_importe', store=True)


    #Cálculo: Si el tipo de concepto tiene porcentaje, el importe es ese porcentaje del salario bruto. Si no, es el importe fijo
    @api.depends('fImporteFijo', 'nomina_id.fSalarioBruto', 'tipo_concepto_id.fPorcentaje')
    def calcular_importe(self):
        for record in self:
            if record.tipo_concepto_id.fPorcentaje > 0:
                record.fImporte = record.nomina_id.fSalarioBruto * record.tipo_concepto_id.fPorcentaje / 100
            else:
                record.fImporte = record.fImporteFijo

    #Validación: Valido que no este en blanco el nombre
    @api.constrains('sNombre')
    def validar_nombre(self):
        for record in self:
            nombre = record.sNombre.strip()
            if not nombre:
                raise ValidationError('El nombre no puede estar en blanco')
            

    #Validación: El importe fijo no es negativo, y es funcional con el tipo de concepto
    @api.constrains('fImporteFijo', 'tipo_concepto_id')
    def validar_importe_fijo(self):
        for record in self:
            if record.fImporteFijo < 0:
                raise ValidationError('El importe fijo no puede ser negativo')
            if record.tipo_concepto_id.fPorcentaje > 0 and record.fImporteFijo != 0:
                raise ValidationError('Este tipo se calcula por porcentaje, deja el importe fijo en 0')
            if record.tipo_concepto_id.fPorcentaje == 0 and record.fImporteFijo <= 0:
                raise ValidationError('Este tipo no tiene porcentaje, indica un importe fijo mayor que 0')


    tipo_concepto_id = fields.Many2one('rrhh_upo.tipo_concepto','Tipo de concepto',required=True)
    nomina_id = fields.Many2one('rrhh_upo.nomina','Nómina',required=True)

    #PREGUNTA AURELIO: meto nomina_id en el unique?
    _sql_constraints =[('concepto_unico', 'UNIQUE(sNombre)', 'Ya existe un concepto ...')]

    