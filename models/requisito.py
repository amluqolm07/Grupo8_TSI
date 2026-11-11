# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Requisito(models.Model):
    _name = 'rrhh_upo.requisito'
    _description = 'Requisito de una oferta'

    name = fields.Char(string="Nombre", required=True)
    motivo = fields.Text(string="Motivo", help='Explica por qué es necesario este requisito para la oferta.')

    oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo',string="Oferta de Empleo",required=True)
    aptitud_ids = fields.Many2many('hr.skill',string="Aptitudes REQUERIDAS para el empleo")
    lenguaje_programacion_ids = fields.Many2many('rrhh_upo.lenguaje_programacion',string="Lenguajes de programación REQUERIDOS para el empleo")
    titulo_idioma_ids = fields.Many2many('rrhh_upo.titulo_idioma',string="Títulos de idioma REQUERIDOS para el empleo")
    titulo_academico_ids = fields.Many2many('hr.recruitment.degree',string="Títulos académicos REQUERIDOS para el empleo")