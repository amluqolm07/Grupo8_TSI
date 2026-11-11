# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoContrato(models.Model):
    _name = 'rrhh_upo.tipo_contrato'
    _description = 'Tipo de contrato'
    _rec_name = 'name'

    
    sNombre= fields.Char(string='Nombre del tipo de contrato', size=30, required=True, help = 'Introduce el nombre del tipo de contrato')
    sDescripcion = fields.Text()
    #Por defecto lo pongo en 0, esto significa "contrato indefinido", ya que un indefinido no tiene duración
    iDuracion = fields.Integer(string='Duración en meses', size=2, required=True, default=0, help ='Introduce la duración del contrato (Si es indefinido ponlo a 0)')
    #Es el tipo de contrato
    name = fields.Selection([
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('formacion', 'Formación'),
        ('practicas', 'Prácticas'),
    ], string='Tipo', required=True)


    contrato_ids = fields.One2many('rrhh_upo.contrato','tipo_contrato_id','Contrato')
    
    _sql_constraints =[('tipo_contrato_unico','UNIQUE(name)','Ya existe ese tipo de contrato')]

    #Validación: Valido que no este en blanco
    @api.constrains('sNombre')
    def validar_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre no puede estar en blanco')
           

    #Validación: Valido que indefinido tenga duración 0 meses (como explique al principio) y que un contrato no indefinido no este en 0 meses
    @api.constrains('iDuracion', 'name')
    def validar_duracion(self):
        for record in self:
            if record.iDuracion < 0:
                raise models.ValidationError('La duración del contrato no puede ser negativa')
            if record.name == 'indefinido' and record.iDuracion !=0:
                raise models.ValidationError('Un contrato indefinido no tiene duración, ponlo en 0')
            if record.name != 'indefinido' and record.iDuracion <= 0:
                raise models.ValidationError('La duración debe ser mayor que 0 meses')

    #Si selecciono indefinido se pone de forma automática duración 0
    @api.onchange('name')
    def onchange_tipo(self):
        if self.name == 'indefinido':
            self.iDuracion = 0