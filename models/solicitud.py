# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Solicitud(models.Model):
    
    _name = 'rrhh_upo.solicitud'
    _description = 'Solicitud'
    
    name = fields.Datetime(string='Fecha de solicitud', required=True, default=fields.Datetime.now)
    concepto = fields.Text()
    estado = fields.Selection([('pendiente', 'Pendiente'),
                            ('aprobada', 'Aprobada'),
                            ('rechazada', 'Rechazada')], default='pendiente')
    cv = fields.Binary('Curriculum Vitae')
    
    # persona_id = fields.Many2one('rrhh_upo.persona', string='Persona', required=True)
    # oferta_empleo_id = fields.Many2one('rrhh_upo.oferta_empleo', string='Oferta de Empleo', required=True)
    # stand_id = fields.Many2one('rrhh_upo.stand', string='Stand', required=True)
    
    # entrevista_ids = fields.One2many('rrhh_upo.entrevista', 'solicitud_id', 'Entrevistas de la solicitud')
    # contrato_ids = fields.One2many('rrhh_upo.contrato', 'solicitud_id', 'Contratos de la solicitud')
    # historial_ids = fields.One2many('rrhh_upo.historial', 'solicitud_id', 'Historial de la solicitud')
    # Titulo academico es many to many con una relacion intermedia 
    
    
    
    def btn_submit_to_pendiente(self):
        self.write({'estado': 'pendiente'})     
        
    def btn_submit_to_aprobada(self):
        self.write({'estado': 'aprobada'})
        
    def btn_submit_to_rechazada(self):
        self.write({'estado': 'rechazada'})
        
    @api.constrains('concepto')
    def _check_concepto(self):
        for record in self:
            if record.concepto and len(record.concepto) < 10:
                raise models.ValidationError("El concepto debe tener al menos 10 caracteres.")
            
    @api.constrains('name')
    def _check_fecha_solicitud(self):
        for record in self:
            if record.name > fields.Datetime.now():
                raise models.ValidationError("La fecha de solicitud no puede ser futura.")

    @api.onchange('name')
    def _onchange_name(self):
        if self.name > fields.Datetime.now():
            self.name = fields.Datetime.now()