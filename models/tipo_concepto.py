from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TipoConcepto(models.Model):
    _name = 'rrhh_upo.tipo_concepto'
    _description = 'Tipo de concepto'
    #Con este ajuste le indico a Odoo que nombre quiero que muestre en los registros.
    _rec_name = 'sNombre'

    #Relaciones de tipo de concepto

    #Según los apuntes esta relación es opcional, pero la he querido reflejar. Solo funciona si existe concepto.
    o2mConceptos = fields.One2many('rrhh_upo.concepto', 'm2oTipoConcepto', string='Conceptos')

    #Declaración de los campos y validaciones básicas:

    #Validación: El usuario debe escribir texto, es obligatorio.
    sCodigo = fields.Char(string='Código', required=True)

    #Validación: El usuario debe escribir un número decimal entre 0 y 100. Por defecto viene en 0.
    fPorcentaje = fields.Float(string='Porcentaje (%)', digits=(5, 2), default=0.0)

    #Validación: El usuario debe escribir texto, es obligatorio rellenarlo.
    sNombre = fields.Char(string='Nombre', required=True)

    #Validación: El usuario debe escribir texto y es opcional.
    sDescripcion = fields.Text(string='Descripción')

    #Validación: Solo admite booleanos True = deducción (resta) y False = no es deducción (suma). Por defecto False.
    bEsDeduccion = fields.Boolean(string='Es deducción', default=False)
    
    #Metodos con validaciones:

    #Validación: Valido tanto que no este en blanco, como su longidud y duplicado.
    @api.constrains('sCodigo')
    def validar_codigo(self):
        for puntero in self:
            codigo = puntero.sCodigo.strip()
            if not codigo:
                raise ValidationError('El código no puede estar en blanco')
            if len(codigo) > 10:
                raise ValidationError('El código no puede superar los 10 caracteres')
            codigo_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('sCodigo', '=ilike', codigo),
            ])
            if codigo_repe:
                raise ValidationError('Ya existe un tipo de concepto con el mismo código')

    #Validación: Valido tanto que no este en blanco, como su longidud y duplicado.
    @api.constrains('sNombre')
    def validar_nombre(self):
        for puntero in self:
            nombre = puntero.sNombre.strip()
            if not nombre:
                raise ValidationError('El nombre no puede estar en blanco')
            if len(nombre) > 35:
                raise ValidationError('El nombre no puede superar los 35 caracteres')
            nombre_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('sNombre', '=ilike', nombre),
            ])
            if nombre_repe:
                raise ValidationError('Ya existe un tipo de concepto con el mismo nombre')
            
    #Validación: El porcentaje debe estar entre 0 y 100.
    @api.constrains('fPorcentaje')
    def validar_porcentaje(self):
        for puntero in self:
            if not 0 <= puntero.fPorcentaje <= 100:
                raise ValidationError('El porcentaje debe estar entre 0 y 100')