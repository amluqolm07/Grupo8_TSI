# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Matricula(models.Model):
    
    _name = 'rrhh_upo.matricula'
    _description = 'Matrícula'
    
    name = fields.Char(string='Curso académico', help = "Curso academico", required=True)
    fecha_matricula = fields.Date('Fecha de matrícula', required=True)
    estado = fields.Selection([('pendiente', 'Pendiente'),
                               ('pagado', 'Pagado'),
                                ('anulada', 'Anulada')], 'Estado de la matrícula', required=True)
    # Añadir creditos matriculados que es un atributo calculado que suma los creditos de las asignaturas matriculadas
    
    expediente_id = fields.Many2one('rrhh_upo.expediente', string='Expediente', required=True)
    # alumno_id = fields.Many2one('rrhh_upo.alumno', string='Alumno', required=True)
    
    matricula_contiene_asignatura_ids = fields.One2many('rrhh_upo.matricula_contiene_asignatura', 'matricula_id', 'Matriculas que contienen la asignatura')
