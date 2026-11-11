# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PuestoTrabajo(models.Model):
    _inherit = 'hr.job'
    categoria_profesional = fields.Char(string="Categoría profesional")
    
    oferta_empleo_ids = fields.One2many('rrhh_upo.oferta_empleo','puesto_trabajo_id',string="Ofertas de Empleo")
    empleado_ids = fields.One2many('rrhh_upo.empleado','puesto_trabajo_id',string="Empleados")