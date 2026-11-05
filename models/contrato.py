# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from datetime import date

class Contrato(models.Model):
    _name = 'rrhh_upo.contrato'
    _description = 'Contrato'
    _rec_name = 'sReferencia'

    
    sReferencia = fields.Char(string='Referencia', size=10, required=True, help='Introduce una referencia identificativa para el contrato')
    dFechaInicio = fields.DateTime(string='Fecha de inicio', required=True, help='Introduce la fecha de inicio del contrato')
    #Un contrato indefinido no tiene fecha de fin
    dFechaFin = fields.DateTime(string='Fecha de fin',help='Introduce la fecha de finalización del contrato (Un contrato indefinido no tiene fecha de fin)')
    #True = activo y False = finalizado (nos referimos al estado del contrato)
    bActivo = fields.Boolean(string='Activo', default=True)
    fSalarioBase = fields.Float(string='Salario base', size=6,required=True, digits=(10, 2), help='Introduce el salario base del contrato')


    #Validación: La referencia no está en blanco
    @api.constrains('sReferencia')
    def validar_referencia(self):
        for record in self:
            referencia = record.sReferencia.strip()
            if not referencia:
                raise ValidationError('La referencia no puede estar en blanco')
            
    
    #Validación: El salario base debe ser mayor que 0
    @api.constrains('fSalarioBase')
    def validar_salario_base(self):
        for record in self:
            if record.fSalarioBase <= 0:
                raise ValidationError('El salario base tiene que ser mayor que 0')
            
    #Validación: Validaciones de la lógica de las fechas y su relacion con el tipo de contrato asociado
    @api.constrains('dFechaInicio', 'dFechaFin', 'tipo_contrato_id')
    def validar_fechas(self):
        for record in self:
            if record.dFechaFin and record.dFechaFin <= record.dFechaInicio:
                raise ValidationError('La fecha de fin debe ser posterior a la de inicio')
            if record.tipo_contrato_id.sTipo == 'indefinido' and record.dFechaFin:
                raise ValidationError('Un contrato indefinido no tiene fecha de fin')
            if record.tipo_contrato_id.sTipo != 'indefinido' and not record.dFechaFin:
                raise ValidationError('Un contrato no indefinido necesita fecha de fin')

    #Validación: Un contrato con fecha de fin ya caducada no puede seguir activo
    @api.constrains('bActivo', 'dFechaFin')
    def validar_estado(self):
        for record in self:
            if record.bActivo and record.dFechaFin and record.dFechaFin < date.today():
                raise ValidationError('Un contrato cuya fecha de fin ya pasó no puede seguir marcado como activo')


    tipo_contrato_id = fields.Many2one('rrhh_upo.tipo_contrato','Tipo de contrato',required=True)
    nomina_ids = fields.One2many('rrhh_upo.nomina','Nómina')
    solicitud_id = fields.Many2one('rrhh_upo.solicitud','Solicitud',required=True)

    _sql_constraints =[('contrato_unico', 'UNIQUE(sReferencia)', 'Ya existe un contrato con esa referencia')]

   
    