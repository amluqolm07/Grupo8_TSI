# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Grado(models.Model):
    
    _name = 'rrhh_upo.grado'
    _description = 'Grado'
    
    name = fields.Char(string='ID', help = "ID del grado", size=7, required=True)
    nombre = fields.Char('Nombre', help = "Nombre del grado", required=True)
    rama = fields.Selection([('ingenieria', 'Ingeniería'),
                             ('ciencias', 'Ciencias'),
                             ('humanidades', 'Humanidades'),
                             ('salud', 'Salud'),
                             ('sociales', 'Sociales')], 'Rama de estudio',required=True)

    
    asignatura_ids = fields.One2many('rrhh_upo.asignatura', 'grado_id', 'Asignaturas del grado')
    departamento_ids = fields.One2many('rrhh_upo.departamento', 'grado_id', 'Departamentos del grado')
    expediente_ids = fields.One2many('rrhh_upo.expediente', 'grado_id', 'Expedientes del grado')
    
    # pdi_ids = fields.many2many('rrhh_upo.pdi', string='PDI del grado')
    
    _sql_constraints = [('rrhh_upo_grado_nombre_unique', 'UNIQUE(nombre)', 'El nombre del grado debe ser único.'),
                        ('rrhh_upo_grado_name_unique', 'UNIQUE(name)', 'El ID del grado debe ser único.')]
    
    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper().strip()
            if len(self.name) < 7:
                return {
                    'value': {'name': ''},
                    'warning': {
                        'title': 'ID demasiado corto',
                        'message': 'El ID del grado debe tener al menos 7 caracteres.'
                    }
                }
            
    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if len(record.name) != 7:
                raise models.ValidationError("El ID del grado debe tener exactamente 7 caracteres.")