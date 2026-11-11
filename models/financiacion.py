# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Financiacion(models.Model):
    
    _name = 'rrhh_upo.financiacion'
    _description = 'Financiación'
    
    name = fields.Date(string='Fecha de acuerpo', help = "Fecha de acuerdo de financiación", required=True)
    importe = fields.Float('Importe', required=True)
    descripcion = fields.Text()
    estado = fields.Selection([('solicitada', 'Solicitada'),
                            ('concedida', 'Concedida'),
                            ('en_proceso', 'En Proceso'),
                            ('rechazada', 'Rechazada')], default='solicitada', required=True)
    
    investigacion_id = fields.Many2one('rrhh_upo.investigacion', string='Investigación', required=True)
    # entidad_externa_id = fields.Many2one('rrhh_upo.entidad_externa', string='Entidad Externa', required=True)