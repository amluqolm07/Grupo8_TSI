# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Asignaturas(models.Model):
    
    _name = 'rrhh_upo.asignatura'
    _description = 'Asignaturas'
    
    name = fields.Char(string='ID', help = "ID de la asignatura", required=True)
    creditos = fields.Integer('Créditos', required=True)
    curso = fields.Integer('Curso', required=True)
    tipo = fields.Selection([('obligatoria', 'Obligatoria'), 
                             ('optativa', 'Optativa'),
                             ('basica', 'Basica')], 'Tipo de asignatura',required=True)
    nombre = fields.Char('Nombre', required=True)
    cuatrimestre = fields.Selection([('1', 'Primer cuatrimestre'), 
                                   ('2', 'Segundo cuatrimestre'),
                                   ('0', 'Anual')], required=True)
    
    grado_id = fields.Many2one("rrhh_upo.grado", string="Grado")
    
    matricula_contiene_asignatura_ids = fields.One2many('rrhh_upo.matricula_contiene_asignatura', 'asignatura_id', 'Matriculas que contienen la asignatura')
    # sesion_ids = fields.One2many('rrhh_upo.sesion', 'asignatura_id', 'Sesiones de la asignatura')
    
    _sql_constraints = [('rrhh_upo_asignatura_name_unique', 'UNIQUE(name)', 'El ID de la asignatura debe ser único.')]
    
    @api.constrains('creditos')
    def _check_creditos(self):
        for record in self:
            if record.creditos <= 0 or record.creditos > 12:
                raise models.ValidationError("Los créditos de la asignatura deben ser entre 1 y 12.")
            
    @api.constrains('curso')
    def _check_curso(self):
        for record in self:
            if record.curso < 1 or record.curso > 4:
                raise models.ValidationError("El curso de la asignatura debe ser entre 1 y 4.")