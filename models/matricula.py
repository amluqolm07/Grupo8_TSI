# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Matricula(models.Model):
    
    _name = 'rrhh_upo.matricula'
    _description = 'Matrícula'
    
    name = fields.Datetime(string='Curso académico', help = "Fecha de matrícula del estudiante", required=True)