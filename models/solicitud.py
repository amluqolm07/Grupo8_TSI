# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Solicitud(models.Model):
    
    _name = 'rrhh_upo.solicitud'
    _description = 'Solicitud'
    
    name = fields.Datetime(string='Fecha de solicitud', required=True, default=fields.Datetime.now)
    concepto = fields.Text()
    estado = fields.Selection([('pendiente', 'Pendiente'),
                               ('en_proceso', 'En Proceso'),
                            ('aprobada', 'Aprobada'),
                            ('rechazada', 'Rechazada')], default='pendiente', required=True)
    cv = fields.Binary('Curriculum Vitae')
    
    # persona_id = fields.Many2one('rrhh_upo.persona', string='Persona', required=True)
    # oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo', string='Oferta de Empleo', required=True)
    # stand_id = fields.Many2one('rrhh_upo.stand', string='Stand', required=True)
    
    # entrevista_ids = fields.One2many('rrhh_upo.entrevista', 'solicitud_id', 'Entrevistas de la solicitud')
    # contrato_ids = fields.One2many('rrhh_upo.contrato', 'solicitud_id', 'Contratos de la solicitud')
    # historial_ids = fields.One2many('rrhh_upo.historial', 'solicitud_id', 'Historial de la solicitud')
    # Titulo academico es many to many con una relacion intermedia 