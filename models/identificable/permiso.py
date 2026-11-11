
# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

class Permiso(models.Model):
    _name = 'rrhh_upo.permiso'
    _description = 'Permisos que aportan funcionalidades dentro del sistema.'
    _sql_constraints = [('nombre_unique', 'UNIQUE(sNombre)', 'El nombre identificador ya existe.')]
    
    rol_ids = fields.Many2many('rrhh_upo.rol', string='Roles', relation='rrhh_upo_permiso_rol_rel')
    
    name = fields.Char(string='Nombre Identificador', required=True)
    sDescriptor = fields.Text(string='Descriptor', help='Permiso para...')
    active = fields.Boolean(string='Permiso en Activo', default=True, required=True)
    
    
    def action_bloquear(self):
            
            for record in self:
                if record.active:
                    record.active = False
                    
                else:
                    raise UserError('El permiso ya se encuentra bloqueado.')
    
    
    def action_desbloquear(self):
        
        for record in self:
            if not record.active:
                record.active = True
                
            else:
                raise UserError('El permiso ya se encuentra activo.')
