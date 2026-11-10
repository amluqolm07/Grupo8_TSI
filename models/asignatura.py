# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Asignaturas(models.Model):
    
    _name = 'rrhh_upo.asignatura'
    _description = 'Asignaturas'
    
    name = fields.Char(string='ID', help = "ID de la asignatura", required=True)
    creditos = fields.Integer(string='Créditos', required=True)
    curso = fields.Integer(string='Curso', required=True)
    tipo = fields.Selection([('obligatoria', 'Obligatoria'), 
                             ('optativa', 'Optativa'),
                             ('basica', 'Basica')], required=True)
    nombre = fields.Char(string='Nombre', help = "Nombre de la asignatura", required=True)
    
    matricula_contiene_asignatura_ids = fields.One2many('rrhh_upo.matricula_contiene_asignatura', 'asignatura_id', 'Matriculas que contienen la asignatura')