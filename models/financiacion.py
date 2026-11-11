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
    
    
    def btn_submit_to_solicitada(self):
        self.write({'estado': 'solicitada'})

    def btn_submit_to_en_proceso(self):
        self.write({'estado': 'en_proceso'})

    def btn_submit_to_concedida(self):
        self.write({'estado': 'concedida'})

    def btn_submit_to_rechazada(self):
        self.write({'estado': 'rechazada'})
        
    @api.constrains('importe')
    def _check_importe(self):
        for record in self:
            if record.importe <= 0:
                raise models.ValidationError('El importe debe ser mayor que 0.')
            
    @api.onchange('name', 'investigacion_id')
    def _onchange_fecha_acuerdo(self):
        if self.name and self.investigacion_id and self.name < self.investigacion_id.fecha_inicio:
            return {
                'warning': {
                    'title': 'Revisa la fecha',
                    'message': 'La fecha del acuerdo es anterior al inicio de la investigación.'
                }
            }
            