
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class Empleado(models.Model):
    _inherits = {'rrhh_upo.persona' : 'persona_id'}
    _name = 'rrhh_upo.empleado'
    _description = 'Empleado dentro de la UPO.'
    _sql_constraints = [('seguridadSocial_unique', 'UNIQUE(sSeguridadSocial)', 'El número de la Seguridad Social ya está registrado.')]
    
    persona_id = fields.Many2one('rrhh_upo.persona', string='Persona Relacionada', required=True, index=True)
    
    ciudadResidencia_id = fields.Many2one('res.country.state', string='Ciudad de Residencia', ondelete='restrict', index=True)
    contrato_ids = fields.One2many('rrhh_upo.contrato', string='Contratos Laborales', inverse_name='empleado_id')
    historialLaboral_ids = fields.One2many('rrhh_upo.historial_laboral', string='Historial Laboral', inverse_name='empleado_id')
    cita_ids = fields.Many2many('rrhh_upo.cita', string='Cita', relation='rrhh_upo_empleado_cita_rel')
    
    sSeguridadSocial = fields.Char(string='Número de la Seguridad Social', required=True)
    sDireccionResidencia = fields.Char(string='Direccion del Domicilio de Residencia')
    sFuncion = fields.Text(string='Función', help='Breve descripción de las funciones.')
    iLongevidad = fields.Integer(string='Días con Contrato', compute='_compute_longevidad', readonly=True, store=False)
    fSalario = fields.Float(string='Sueldo', compute='_compute_salario', digits=(10, 2), readonly=True, store=False)
    
    
    @api.depends('historialLaboral_ids.dFechaInicio')
    def _compute_longevidad(self):
        hoy = date.today()
        
        for record in self:
            if record.historialLaboral_ids:
                fechas_hist = record.historialLaboral_ids.mapped('dFechaInicio')
                
                if fechas_hist:
                    record.iLongevidad = (hoy - min(fechas_hist)).days
    
    
    @api.depends('contrato_ids.fSalarioBase')
    def _compute_salario(self):
        
        for record in self:
            record.fSalarioBase = record.contratos_ids[0].fSalarioBase
    