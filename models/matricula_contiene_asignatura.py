# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MatriculaContieneAsignatura(models.Model):
    _name = 'rrhh_upo.matricula_contiene_asignatura'
    _description = 'Matrícula contiene asignatura'

    nota = fields.Float(string='Nota', required=True) 
    
    asignatura_id = Many2one("rrhh_upo.asignatura", string="Asignatura")
    matricula_id = Many2one("rrhh_upo.matricula", string="Matrícula")
