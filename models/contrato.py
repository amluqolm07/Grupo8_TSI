from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Contrato(models.Model):
    _name = 'rrhh_upo.contrato'
    _description = 'Contrato'
    _rec_name = 'sReferencia'

    #Relaciones del contrato:

    #Un contrato tiene un tipo. No se puede borrar un tipo que tenga contratos por eso tenemos ondelete='restrict'.
    m2oTipoContrato = fields.Many2one('rrhh_upo.tipo_contrato', string='Tipo de contrato', required=True, index=True, ondelete='restrict')
    #Según los apuntes esta relación es opcional, pero la he querido reflejar.
    o2mNominas = fields.One2many('rrhh_upo.nomina', 'm2oContrato', string='Nóminas')
    #Un contrato nace de una solicitud. No se puede borrar una solicitud que ya ha generado un contrato por eso tenemos ondelete='restrict' .
    m2oSolicitud = fields.Many2one('rrhh_upo.solicitud', string='Solicitud', required=True, index=True, ondelete='restrict')

    #Declaración de los campos y validaciones básicas:

    #Validación: El usuario debe escribir un código, es obligatorio. Este codigo sirve para diferenciar los contratos.
    sReferencia = fields.Char(string='Referencia', required=True)

    #Validación: El usuario debe introducir una fecha válida y de forma obligatoria. Por defecto, la fecha de hoy.
    dFechaInicio = fields.Date(string='Fecha de inicio', required=True, default=fields.Date.today)

    #Validación: El usuario debe introducir una fecha válida, es opcional (un contrato indefinido no tiene fecha de fin).
    dFechaFin = fields.Date(string='Fecha de fin')

    #Validación: Solo admite booleanos True = activo y False = finalizado (nos referimos al estado del contrato). Por defecto True.
    bActivo = fields.Boolean(string='Activo', default=True)

    #Validación: El usuario debe introducir un número decimal con dos decimales, es obligatorio.
    fSalarioBase = fields.Float(string='Salario base', required=True, digits=(10, 2))

    #Metodos con validaciones:

    #Validación: La referencia no está en blanco, no supera los 20 caracteres y no se duplica.
    @api.constrains('sReferencia')
    def validar_referencia(self):
        for puntero in self:
            referencia = puntero.sReferencia.strip()
            if not referencia:
                raise ValidationError('La referencia no puede estar en blanco')
            if len(referencia) > 20:
                raise ValidationError('La referencia no puede superar los 20 caracteres')
            referencia_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('sReferencia', '=ilike', referencia),
            ])
            if referencia_repe:
                raise ValidationError('Ya existe un contrato con la misma referencia')
    
    #Validación: El salario base debe ser mayor que 0.
    @api.constrains('fSalarioBase')
    def validar_salario_base(self):
        for puntero in self:
            if puntero.fSalarioBase <= 0:
                raise ValidationError('El salario base tiene que ser mayor que 0')
            
    #Validación: Validaciones de la lógica de las fechas y su relacion con el tipo de contrato asociado.
    @api.constrains('dFechaInicio', 'dFechaFin', 'm2oTipoContrato')
    def validar_fechas(self):
        for puntero in self:
            if puntero.dFechaFin and puntero.dFechaFin <= puntero.dFechaInicio:
                raise ValidationError('La fecha de fin debe ser posterior a la de inicio')
            if puntero.m2oTipoContrato.sTipo == 'indefinido' and puntero.dFechaFin:
                raise ValidationError('Un contrato indefinido no tiene fecha de fin')
            if puntero.m2oTipoContrato.sTipo != 'indefinido' and not puntero.dFechaFin:
                raise ValidationError('Un contrato no indefinido necesita fecha de fin')

    #Validación: Un contrato con fecha de fin ya caducada no puede seguir activo.
    @api.constrains('bActivo', 'dFechaFin')
    def validar_estado(self):
        for puntero in self:
            if puntero.bActivo and puntero.dFechaFin and puntero.dFechaFin < date.today():
                raise ValidationError('Un contrato cuya fecha de fin ya pasó no puede seguir marcado como activo')