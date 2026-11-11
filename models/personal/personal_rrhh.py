
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PersonalRRHH(models.Model):
    _inherits = {'rrhh_upo.empleado' : 'empleado_id'}
    _name = 'rrhh_upo.personal_rrhh'
    _description = 'Personal de Recursos Humanos'
    
    empleado_id = fields.Many2one('rrhh_upo.empleado', string='Empleado Relacionado', required=True, index=True)
    
    entrevista_ids = fields.Many2many('rrhh_upo.entrevista', string='Entrevista', relation='rrhh_upo_personal_rrhh_entrevista_rel')
    ayuda_ids = fields.Many2many('rrhh_upo.ayuda', string='Ayuda', relation='rrhh_upo_personal_rrhh_ayuda_rel')
    stand_ids = fields.Many2many('rrhh_upo.stand', string='Stand', relation='rrhh_upo_personal_rrhh_stand_rel')
    
    iEntrevistas = fields.Integer(string='Entrevistas Asignadas', compute='_compute_entrevistas', readonly=True, store=False)
    iAyudas = fields.Integer(string='Ayudas Asignadas', compute='_compute_ayudas', readonly=True, store=False)
    iStands = fields.Integer(string='Stands Asignados', compute='_compute_stands', readonly=True, store=False)
    sAreaEspecializacion = fields.Selection([('reclutamiento', 'Atracción y Selección de Talento'),
                                             ('academica', 'Gestión de Ayudas Académicas'),
                                             ('eventos', 'Asistente de Eventos'),
                                             ('general', 'General')], string='Área de Especialización', required=True)
    sNivelIngles = fields.Selection([('b1', 'B1 - Intermedio'),
                                     ('b2', 'B2 - Alto'),
                                     ('c1', 'C1 - Avanzado'),
                                     ('c2', 'C2 - Experto')], string='Nivel de Inglés', required=True)
    
    
    @api.depends('entrevista_ids', 'ayuda_ids', 'stand_ids')
    def _compute_entrevistas(self):
        
        for record in self:
            record.iEntrevistas = len(record.entrevista_ids)
            record.iAyudas = len(record.ayuda_ids)
            record.iStands = len(record.stand_ids)
