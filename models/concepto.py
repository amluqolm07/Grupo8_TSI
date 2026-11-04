from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Concepto(models.Model):
    _name = 'rrhh_upo.concepto'
    _description = 'Concepto'
    #Con este ajuste le indico a Odoo que nombre quiero que muestre en los registros.
    _rec_name = 'sNombre'

    #Relaciones del concepto:

    #Un concepto pertenece a una nómina. Si se borra la nómina, se borran sus conceptos de ahi viene la instrucción ondelete='cascade'.
    m2oNomina = fields.Many2one('rrhh_upo.nomina', string='Nómina', required=True, index=True, ondelete='cascade')
    #Un concepto tiene un tipo. No se puede borrar un tipo que tenga conceptos por eso pongo ondelete='restrict'.
    m2oTipoConcepto = fields.Many2one('rrhh_upo.tipo_concepto', string='Tipo de concepto', required=True, index=True, ondelete='restrict')


    #Declaración de los campos y validaciones básicas:

    #Validación: El usuario debe escribir texto, es obligatorio.
    sNombre = fields.Char(string='Nombre', required=True)

    #Validación: El usuario debe escribir texto y es opcional.
    sDescripcion = fields.Text(string='Descripción')

    #Validación: Número decimal con dos decimales. Esto solo se usa si el tipo de concepto no tiene porcentaje. Por defecto va a 0.
    fImporteFijo = fields.Float(string='Importe fijo', digits=(10, 2), default=0.0)

    #Validación: Campo autocalculado (no lo introduce el usuario). store=True para guardarlo en la BD.
    fImporte = fields.Float(string='Importe', digits=(10, 2), compute='calcular_importe', store=True)

    #Metodos con validaciones y cálculos:

    #Cálculo: Si el tipo de concepto tiene porcentaje, el importe es ese porcentaje del salario bruto. Si no, es el importe fijo.
    @api.depends('fImporteFijo', 'm2oNomina.fSalarioBruto', 'm2oTipoConcepto.fPorcentaje')
    def calcular_importe(self):
        for record in self:
            if record.m2oTipoConcepto.fPorcentaje > 0:
                record.fImporte = record.m2oNomina.fSalarioBruto * record.m2oTipoConcepto.fPorcentaje / 100
            else:
                record.fImporte = record.fImporteFijo

    #Validación: Valido tanto que no este en blanco, como su longidud. No valido duplicados, porque por ejemplo IRPF aparece en todas las nóminas.
    @api.constrains('sNombre')
    def validar_nombre(self):
        for puntero in self:
            nombre = puntero.sNombre.strip()
            if not nombre:
                raise ValidationError('El nombre no puede estar en blanco')
            if len(nombre) > 35:
                raise ValidationError('El nombre no puede superar los 35 caracteres')

    #Validación: El importe fijo no es negativo, y es funcional con el tipo de concepto.
    @api.constrains('fImporteFijo', 'm2oTipoConcepto')
    def validar_importe_fijo(self):
        for puntero in self:
            if puntero.fImporteFijo < 0:
                raise ValidationError('El importe fijo no puede ser negativo')
            if puntero.m2oTipoConcepto.fPorcentaje > 0 and puntero.fImporteFijo != 0:
                raise ValidationError('Este tipo se calcula por porcentaje, deja el importe fijo en 0')
            if puntero.m2oTipoConcepto.fPorcentaje == 0 and puntero.fImporteFijo <= 0:
                raise ValidationError('Este tipo no tiene porcentaje, indica un importe fijo mayor que 0')
    