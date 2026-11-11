# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aptitud(models.Model):
    _inherit = 'hr.skill'

    descripcion = fields.Text(string="Descripción")
    
    requisito_ids = fields.Many2many('rrhh_upo.requisito',string="Requisitos que exigen la aptitud")