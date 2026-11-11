# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LenguajeProgramacion(models.Model):
    _name = 'rrhh_upo.lenguaje_programacion'
    _description = 'Lenguaje de programación'

    name = fields.Char(string="Lenguaje", required=True)
    proposito = fields.Selection([('frontend', 'Frontend'),
                                  ('backend', 'Backend'),
                                  ('movil', 'Móvil'),
                                  ('ia', 'IA'),
                                  ('videojuegos', 'Videojuegos')],"Propósito", required=True)
    
    requisito_ids = fields.Many2many('rrhh_upo.requisito',string="Requisitos que lo incluyen")
