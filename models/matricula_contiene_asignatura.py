# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MatriculaContieneAsignatura(models.Model):
    _name = 'rrhh_upo.matricula_contiene_asignatura'
    _description = 'Matrícula contiene asignatura'

    nota = fields.Float(string='Nota')
    # añadir atributo superada que es un auto-calculado que indica si la asignatura ha sido superada o no (nota >= 5)
    
    asignatura_id = fields.Many2one("rrhh_upo.asignatura", string="Asignatura")
    matricula_id = fields.Many2one("rrhh_upo.matricula", string="Matrícula")
