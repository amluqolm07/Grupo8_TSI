# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class Nomina(models.Model):
    _name = 'rrhh_upo.nomina'
    _description = 'Nómina'
    _rec_name = 'name'

    
    #Autocalculado, además lo voy a usar como PK
    name = fields.Char(string='Nombre de la nómina', compute='generador_nombre_nomina',store=True)
    sPeriodoMes = fields.Selection([
        ('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'),
        ('abril', 'Abril'), ('mayo', 'Mayo'), ('junio', 'Junio'),
        ('julio', 'Julio'), ('agosto', 'Agosto'), ('septiembre', 'Septiembre'),
        ('octubre', 'Octubre'), ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre'),
    ], string='Mes',required=True)
    iPeriodoAnio = fields.Integer(string='Año',required=True, help="Introduce el periodo del año")
    fSalarioBruto = fields.Float(string='Salario bruto', required=True, help="Introduce el salario bruto")
    dFechaEmision = fields.Datetime(string='Fecha de emisión', required=True, help="Introduce la fecha de emisión")
    #Autocalculado
    fTotalDeducciones = fields.Float(string='Total deducciones', compute='calcular_importe',store=True)
    #Autocalculado
    fSalarioNeto = fields.Float(string='Salario neto', compute='calcular_importe',store=True)
    #True = "Emitida", por defecto la nomina esta en False = "Borrador"
    bEmitida = fields.Boolean(string='Emitida', default=False)
    

    contrato_id = fields.Many2one('rrhh_upo.contrato','Contrato',required=True)
    concepto_ids = fields.One2many('rrhh_upo.concepto','nomina_id','Concepto')
    
    
    _sql_constraints =[('nomina_unica','UNIQUE(name)','Este contrato ya tiene una nómina con esa fecha de emisión')]

    #Validación: El periodo del año esta entre el año que se fundo la UPO (1997) y el año actual
    @api.constrains('iPeriodoAnio')
    def validacion_periodo_anio(self):
        for record in self:
            if not 1997 <= record.iPeriodoAnio <= date.today().year: 
                raise models.ValidationError(f'El año debe estar entre 1997 y {date.today().year}')
            
    #Validación: El salario bruto introducido debe ser mayor que 0
    @api.constrains('fSalarioBruto')
    def validacion_salario_bruto(self):
        for record in self:
            if record.fSalarioBruto <= 0:
                raise models.ValidationError('El salario bruto tiene que ser mayor que 0')

    #Validación: Comprueba que la fecha de emisión no esta en el futuro
    @api.constrains('dFechaEmision')
    def validacion_fecha_emision(self):
        for record in self:
            if record.dFechaEmision and record.dFechaEmision > fields.Datetime.now():
                raise models.ValidationError('La fecha de emisión no puede ser futura')

    #Validación: El salario neto no puede ser negativo
    @api.constrains('fSalarioNeto')
    def validacion_salario_neto(self):
        for record in self:
            if record.fSalarioNeto < 0:
                raise models.ValidationError('El salario neto no puede ser negativo')

    #Validación: Se exige que la nómina tenga un concepto
    @api.constrains('bEmitida', 'concepto_ids')
    def validacion_emitida(self):
        for record in self:
                if record.bEmitida and not record.concepto_ids:
                    raise models.ValidationError('Para emitir una nómina necesita un concepto')

    #Cálculo: Calculo salario neto
    @api.depends('fSalarioBruto','concepto_ids.fImporte','concepto_ids.tipo_concepto_id.bEsDeduccion')
    def calcular_importe(self):
        for record in self:
            fTotal_deducciones_temporal = 0.0
            fTotal_extras_temporal = 0.0
            for concepto in record.concepto_ids:
                if concepto.tipo_concepto_id.bEsDeduccion:
                    fTotal_deducciones_temporal += concepto.fImporte
                else:
                    fTotal_extras_temporal += concepto.fImporte
            record.fTotalDeducciones = fTotal_deducciones_temporal
            record.fSalarioNeto = record.fSalarioBruto + fTotal_extras_temporal - fTotal_deducciones_temporal  

    #Calculo: A partir de la fecha de emisión y la referencia del contrato genera un nombre para la nomina
    @api.depends('contrato_id.name', 'dFechaEmision')
    def generador_nombre_nomina(self):
        for record in self:
            referencia = record.contrato_id.name 
            fecha = record.dFechaEmision
            record.name = f'{referencia} - {fecha}'

    #Lo pongo como refuerzo de la validacion de salario bruto
    @api.onchange('fSalarioBruto')
    def onchange_salario_bruto(self):
        if self.fSalarioBruto <= 0:
            return {
            'warning': {'title': 'Salario incorrecto','message': 'El salario bruto debe ser mayor que 0.'}
        }