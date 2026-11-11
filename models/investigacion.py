# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Investigacion(models.Model):
    
    _name = 'rrhh_upo.investigacion'
    _description = 'Investigación'
    
    name = fields.Char(string='Nombre', help = "Nombre de la investigación", required=True)
    fecha_inicio = fields.Date('Fecha de inicio', required=True)
    fecha_fin = fields.Date('Fecha de fin')
    estado = fields.Boolean('En proceso', required=True)
    descripcion = fields.Text()
    # añadir financiacion total, suma de todas las financiaciones
    
    # pdi_ids = fields.Many2many('rrhh_upo.pdi', String='PDI')
    tipo_investigacion_id = fields.Many2one('rrhh_upo.tipo_investigacion', string='Tipo de investigación', required=True)
    
    equipo_trabaja_investigacion_ids = fields.One2many('rrhh_upo.equipo_trabaja_investigacion', 'investigacion_id', 'Equipo de investigación')
    financiacion_ids = fields.One2many('rrhh_upo.financiacion', 'investigacion_id', 'Financiación')