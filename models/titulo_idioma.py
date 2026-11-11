# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TituloIdioma(models.Model):
    _name = 'rrhh_upo.titulo_idioma'
    _description = 'Título de idioma'

    idioma = fields.Char(string="Idioma",required=True)
    nivel = fields.Selection([('A1', 'A1'), ('A2', 'A2'),
                              ('B1', 'B1'), ('B2', 'B2'),
                              ('C1', 'C1'), ('C2', 'C2')],"Nivel",required=True)
    academia = fields.Char(string="Academia",required=True)
    name = fields.Char(compute='_compute_name',string="Nombre del título",store=True)
    requisito_ids = fields.Many2many('rrhh_upo.requisito',string="Requisitos que lo incluyen")

    @api.depends('idioma', 'nivel', 'academia')
    def _compute_name(self):
        for i in self:
            i.name = f"{i.idioma or ''} {i.nivel or ''}-[{i.academia or ''}]"