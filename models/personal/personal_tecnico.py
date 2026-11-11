
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PersonalTecnico(models.Model):
    _inherits = {'rrhh_upo.empleado' : 'empleado_id'}
    _name = 'rrhh_upo.personal_tecnico'
    _description = 'Personal Técnico Evaluador'
    
    empleado_id = fields.Many2one('rrhh_upo.empleado', string='Empleado Relacionado', required=True, index=True)
    
    entrevista_ids = fields.Many2many('rrhh_upo.entrevista', string='Entrevistas', relation='rrhh_upo_personal_tecnico_entrevista_rel')
    
    sEspecialidad = fields.Char(string='Especialidad Técnica')
    bDisponible = fields.Boolean(string='Disponible para Entrevistas', default=True, required=True)
    iEntrevistas = fields.Integer(string='Entrevistas Asignadas', compute='_compute_entrevistas', readonly=True, store=False)
    sNivelExperiencia = fields.Selection([('junior', 'Junior'),
                                          ('medio', 'Nivel Medio'),
                                          ('senior', 'Senior'),
                                          ('lead', 'Avanzado')], required=True)
    
    
    @api.depends('entrevista_ids')
    def _compute_entrevistas(self):
        
        for record in self:
            record.iEntrevistas = len(record.entrevista_ids)
