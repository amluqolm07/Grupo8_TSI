# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Departamento(models.Model):
    
    _name = 'rrhh_upo.departamento'
    _description = 'Departamento'
    
    name = fields.Char(string='Nombre', help = "Nombre del departamento", required=True)
    email = fields.Char('Email', required=True)
    planta = fields.Char('Planta', required=True)
    
    grado_id = fields.Many2one('rrhh_upo.grado', string='Grado', required=True)
    # edificio_id = fields.Many2one('rrhh_upo.edificio', string='Edificio', required=True)
    equipo_investigacion_ids = fields.Many2many('rrhh_upo.equipo_investigacion', string='Equipos de investigación')    
    
    telefono_ids = fields.One2many('rrhh_upo.telefonos_departamentos', 'departamento_id', 'Teléfonos del departamento')
    
    _sql_constraints = [('rrhh_upo_departamento_name_unique', 'UNIQUE(name)', 'El nombre del departamento debe ser único.')]
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if '@' not in record.email or '.' not in record.email.split('@')[-1]:
                raise models.ValidationError('El email del departamento no es válido.')

    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            self.email = self.email.strip().lower()