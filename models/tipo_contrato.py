from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TipoContrato(models.Model):
    _name = 'rrhh_upo.tipo_contrato'
    _description = 'Tipo de contrato'
    #Con este ajuste le indico a Odoo que nombre quiero que muestre en los registros.
    _rec_name = 'sNombre'

    #Relaciones de tipo de contrato

    #Según los apuntes esta relación es opcional, pero la he querido reflejar. Solo funciona si existe contrato.
    o2mContratos = fields.One2many('rrhh_upo.contrato', 'm2oTipoContrato', string='Contratos')


    #Declaración de los campos y validaciones básicas:

    #Validación: El usuario debe escribir texto, es obligatorio rellenarlo.
    sNombre = fields.Char(string='Nombre', required=True)

    #Validación: El usuario debe escribir texto y es opcional.
    sDescripcion = fields.Text(string='Descripción')
    
    #Validación: El usuario debe escribir un número entero (Los meses que dure el contrato).
    #Por defecto lo pongo en 0, esto significa "contrato indefinido", ya que un indefinido no tiene duración.
    iDuracion = fields.Integer(string='Duración (meses)', default=0)

    #Validación: El usuario debe elegir entre las opciones, es obligatorio.
    sTipo = fields.Selection([
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('formacion', 'Formación'),
        ('practicas', 'Prácticas'),
    ], string='Tipo', required=True)

    #Metodos con validaciones

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
                ('sNombre', '=ilike', nombre), #El =ilike lo uso para que compare sin distinguir mayusculas.
            ])
            if nombre_repe:
                raise ValidationError('Ya existe un tipo de contrato con el mismo nombre')

    #Validación: Valido que indefinido tenga duración 0 meses (como explique al principio) y que un contrato no indefinido no este en 0 meses.
    @api.constrains('iDuracion', 'sTipo')
    def validar_duracion(self):
        for puntero in self:
            if puntero.iDuracion < 0:
                raise ValidationError('La duración del contrato no puede ser negativa')
            if puntero.sTipo == 'indefinido' and puntero.iDuracion !=0:
                raise ValidationError('Un contrato indefinido no tiene duración, ponlo en 0')
            if puntero.sTipo != 'indefinido' and puntero.iDuracion <= 0:
                raise ValidationError('La duración debe ser mayor que 0 meses')