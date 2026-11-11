
# -*- coding: utf-8 -*-

from odoo import models, fields

class Rol(models.Model):
    _name = 'rrhh_upo.rol'
    _description = 'Roles que puede adoptar un usuario del sistema.'
    _sql_constraints = [('nombre_unique', 'UNIQUE(sNombre)', 'El nombre identificador ya existe.')]
    
    usuario_ids = fields.Many2many('rrhh_upo.usuario', string='Usuarios', relation='rrhh_upo_usuario_rol_rel')
    permiso_ids = fields.Many2many('rrhh_upo.permiso', string='Permisos Englobados', relation='rrhh_upo_permiso_rol_rel')
    
    name = fields.Char(string='Nombre Identificador', required=True)
    sDescriptor = fields.Text(string='Descriptor', help='Rol requerido para...')
    