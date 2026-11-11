# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Investigacion(models.Model):
    
    _name = 'rrhh_upo.investigacion'
    _description = 'Investigación'
    
    name = fields.Char(string='Nombre', help = "Nombre de la investigación", required=True)
    fecha_inicio = fields.Date('Fecha de inicio', required=True)
    fecha_fin = fields.Date('Fecha de fin')
    estado = fields.Selection([('en_proceso', 'En proceso'), 
                               ('finalizada', 'Finalizada'),
                               ('cancelada', 'Cancelada')], 'Estado', default='en_proceso', required=True)
    descripcion = fields.Text()
    # añadir financiacion total, suma de todas las financiaciones
    
    # pdi_ids = fields.Many2many('rrhh_upo.pdi', String='PDI')
    tipo_investigacion_id = fields.Many2one('rrhh_upo.tipo_investigacion', string='Tipo de investigación', required=True)
    
    equipo_trabaja_investigacion_ids = fields.One2many('rrhh_upo.equipo_trabaja_investigacion', 'investigacion_id', 'Equipo de investigación')
    financiacion_ids = fields.One2many('rrhh_upo.financiacion', 'investigacion_id', 'Financiación')
    
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio > record.fecha_fin:
                raise models.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
            
    @api.constrains('estado', 'fecha_fin')
    def _check_estado_fecha_fin(self):
        for record in self:
            if record.estado == 'finalizada' and not record.fecha_fin:
                raise models.ValidationError("Si la investigación está finalizada, debe especificarse la fecha de fin.")
    
    
    @api.onchange('fecha_inicio', 'fecha_fin')
    def _onchange_fechas(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                return {
                    'value': {'fecha_fin': False},
                    'warning': {
                        'title': 'Fecha de inicio posterior a fecha de fin',
                        'message': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
                    }
                }
                
    def btn_submit_to_en_proceso(self):
        self.write({'estado': 'en_proceso', 'fecha_fin': False})     
            
    def btn_submit_to_finalizada(self):
        self.write({'estado': 'finalizada', 'fecha_fin': fields.Date.today()})
            
    def btn_submit_to_cancelada(self):
        self.write({'estado': 'cancelada'})