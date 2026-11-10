# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Matricula(models.Model):
    
    _name = 'rrhh_upo.matricula'
    _description = 'Matrícula'
    
    name = fields.Char(string='Curso académico', help = "Curso academico", required=True)
    fecha_matricula = fields.Datetime(string='Fecha de matrícula', help = "Fecha de matrícula del estudiante", required=True)
    # Añadir creditos matriculados que es un atributo calculado que suma los creditos de las asignaturas matriculadas
    
    matricula_contiene_asignatura_ids = fields.One2many('rrhh_upo.matricula_contiene_asignatura', 'matricula_id', 'Matriculas que contienen la asignatura')