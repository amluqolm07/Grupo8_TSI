# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Matricula(models.Model):
    
    _name = 'rrhh_upo.matricula'
    _description = 'Matrícula'
    
    name = fields.Datetime(string='Curso académico', help = "Fecha de matrícula del estudiante", required=True)
    
    matricula_contiene_asignatura_ids = fields.One2many('rrhh_upo.matricula_contiene_asignatura', 'matricula_id', 'Matriculas que contienen la asignatura')