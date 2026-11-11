
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Persona(models.Model):
    _name = 'rrhh_upo.persona'
    _description = 'Cualquier persona que interactúa con el sistema.'
    _sql_constraints = [('sDni', 'UNIQUE(sDni)', 'El DNI ya está registrado en el sistema.')]
    _rec_name = 'sDni'
    
    paisResidencia_id = fields.Many2one('res.country', string='País de Residencia')
    
    sDni = fields.Char(string='DNI', help='Ej: 12345678A', size=9, required=True, index=True)
    sNombre = fields.Char(string='Nombre', required=True)
    sPrimerApellido = fields.Char(string='Primer Apellido', required=True)
    sSegundoApellido = fields.Char(string='Segundo Apellido')
    sEmail = fields.Char(string='Correo Electrónico', required=True)
    sTelefono = fields.Char(string='Teléfono', help='Ej: +34 123456789', size=15)
    dFechaNacimiento = fields.Date(string='Fecha de Nacimiento', required=True)
    iEdad = fields.Integer(string='Edad', compute='_compute_edad', readonly=True)
    
    
    @api.constrains('sDni')
    def _check_dni(self):
        regex = r'^\d{8}[A-Z]$'
        
        for record in self:
            if record.sDni:
                if not record.sDni.strip():
                    raise ValidationError('El DNI no puede contener solo espacios.')
                            
                if not re.match(regex, record.sDni):
                    raise ValidationError('Formato de DNI no válido.')
                
                
    @api.constrains('sNombre', 'sPrimerApellido', 'sSegundoApellido')
    def _check_alfabetico(self):
        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'\-]+$"
        
        for record in self:
            campos = {'nombre': record.sNombre,
                      'primer apellido': record.sPrimerApellido,
                      'segundo apellido': record.sSegundoApellido}
            
            for campo, valor in campos:
                if valor:
                    if not valor.strip():
                        raise ValidationError(f"El '{campo}' no puede contener solo espacios.")
                    
                    if not re.match(regex, valor):
                        raise ValidationError(f"El valor del '{campo}' no está permitido.")
                        
    
    @api.constrains('sEmail')
    def _check_email(self):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for record in self:
            if record.sEmail:
                if not record.sEmail.strip():
                    raise ValidationError('El correo electrónico no puede contener solo espacios.')
                
                if not re.match(regex, record.sEmail):
                    raise ValidationError('Formato de correo electrónico no válido.')
                
                
    @api.onchange('sTelefono')
    def _onchange_telefono(self):
        
        if self.sTelefono:
            self.sTelefono = re.sub(r'[\s\-\.\(\)]', '', self.sTelefono)
            
            
    @api.constrains('sTelefono')        
    def _check_telefono(self):
        regex = r'^\+?[0-9]{7,15}$'
        
        for record in self:
            if record.sTelefono:
                if not re.match(regex, record.sTelefono):
                    raise ValidationError('Formato de teléfono no válido.')
        
            
    @api.constrains('dFechaNacimiento')
    def _check_fecha_nacimiento(self):
        hoy = fields.Date.today()
        
        for record in self:
            if record.dFechaNacimiento:
                if record.dFechaNacimiento > hoy:
                    raise ValidationError('La fecha de nacimiento no puede ser posterior a hoy.')
                
                
    @api.depends('dFechaNacimiento')
    def _compute_edad(self):
        hoy = fields.Date.today()
        
        for record in self:
            if record.sFechaNacimiento:
                nac = record.sFechaNacimiento
                
                record.iEdad = hoy.year - nac.year - ((hoy.month, hoy.day) < (nac.month, nac.day))     
                