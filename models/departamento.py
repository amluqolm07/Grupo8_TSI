# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Departamento(models.Model):
    
    _name = 'rrhh_upo.departamento'
    _description = 'Departamento'
    
    name = fields.Char(string='Nombre', help = "Nombre del departamento", required=True)
    email = fields.Char(string='Email', required=True)
    planta = fields.Char(string='Planta', required=True)
    
    grado_id = fields.Many2one('rrhh_upo.grado', string='Grado', required=True)
    # edificio_id = fields.Many2one('rrhh_upo.edificio', string='Edificio', required=True)
    equipo_investigacion_ids = fields.Many2many('rrhh_upo.equipo_investigacion', string='Equipos de investigación')    
    
    telefono_ids = fields.One2many('rrhh_upo.telefonos_departamentos', 'departamento_id', 'Teléfonos del departamento')
    
