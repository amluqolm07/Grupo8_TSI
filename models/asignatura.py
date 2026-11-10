# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Asignaturas(models.Model):
    
    _name = 'grupo8_tsi.asignatura'
    _description = 'Asignaturas'
    
    name = fields.Char(string='ID', help = "ID de la asignatura", required=True)
    creditos = fields.Integer(string='Créditos', required=True)
    curso = fields.Integer(string='Curso', required=True)
    tipo = fields.Selection([('obligatoria', 'Obligatoria'), 
                             ('optativa', 'Optativa'),
                             ('basica', 'Basica')], required=True)
    nombre = fields.Char(string='Nombre', help = "Nombre de la asignatura", required=True)
    
    