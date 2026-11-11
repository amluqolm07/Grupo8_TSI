
# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

class Alumno(models.Model):
    _inherits = {'rrhh_upo.persona' : 'persona_id'}
    _name = 'rrhh_upo.alumno'
    _description = 'Alumno de la UPO'
    
    persona_id = fields.Many2one('rrhh_upo.persona', string='Persona Relacionada', required=True, index=True)
    
    expediente_ids = fields.One2Many('rrhh_upo.expediente', string='Expediente', inverse_name='alumno_id') 
    sesion_ids = fields.Many2many('rrhh_upo.sesion', string='Sesiones', relation='rrhh_upo_alumno_sesion_rel')
    #gradosMatriculados_ids Es importante conocer matrícula, trabajando en ello :p
    
    bDiscapacidad = fields.Boolean(string='Discapacidad', required=True)
    active = fields.Boolean(string='Estudiante Activo', default=True, required=True, readonly=True)
    sTipoAcceso = fields.Selection([('EBAU', 'Selectividad'),
                                    ('CFGS', 'Ciclo Formativo'),
                                    ('Erasmus', 'Estudiante Extranjero')], string='Tipo de Acceso')
    
    
    def action_bloquear(self):
            
        for record in self:
            if record.active:
                record.active = False
                
            else:
                raise UserError('El alumno no estaba en activo.')
    
    
    def action_desbloquear(self):
        
        for record in self:
            if not record.active:
                record.active = True
                
            else:
                raise UserError('El alumno ya estaba en activo.')
