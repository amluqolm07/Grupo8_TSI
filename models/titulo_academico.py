# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TituloAcademico(models.Model):
    _inherit = 'hr.recruitment.degree'
    rama = fields.Char(string="Rama", help='Rama de conocimiento a la que pertenece la titulación '
                                           '(por ejemplo: Ingeniería, Ciencias de la Salud, '
                                           'Artes y Humanidades, Ciencias Sociales).')
    requisito_ids = fields.Many2many('rrhh_upo.requisito',string="Requisitos que lo incluyen")
    solicitud_ids = fields.One2many('rrhh_upo.solicitud','titulo_academico_id', string="Titulos obtenidos por la solicitud")