
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PersonalExterno(models .Model):
    _inherits = {'rrhh_upo.empleado' : 'empleado_id'}
    _name = 'rrhh_upo.personal_externo'
    _description = 'Personal Externo Subcontratado'
    
    empleado_id = fields.Many2one('rrhh_upo.empleado', string='Empleado Relacionado', required=True, index=True)
    
    entidadExterna_id = fields.Many2one('rrhh_upo.entidad_externa', string='Subcontrata', required=True, index=True)
    
    dFechaFinAcceso = fields.Date(string='Fecha Fin de Acceso al Campus', required=True)
    bPrevencionRiesgos = fields.Boolean(string='Homologado en Preveción de Riesgos Laborales', default=False, required=True)
    sServicio = fields.Selection([('limpieza', 'Servicio de Limpieza'),
                                  ('jardineria', 'Jardinería y Paisajismo'),
                                  ('seguridad', 'Vigilancia y Seguridad'),
                                  ('mantenimiento', 'Mantenimiento de Instalaciones'),
                                  ('catering', 'Servicio de Catering')], string='Tipo de Servicio', required=True)
    
    
    @api.constraints('dFechaFinAcceso')
    def check_fecha_fin_acceso(self):
        
        for record in self:
            if record.dFechaFinAcceso and record.contrato_ids:               
                if record.contrato_ids[0].dFechaInicio > record.dFechaFinAcceso:
                    raise ValidationError('La fecha de fin de acceso al campus es anterior al inicio del contrato.')
