# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Historial(models.Model):

    _name = 'rrhh_upo.historial'
    _description = 'Historial de la solicitud'

    solicitud_id = fields.Many2one('rrhh_upo.solicitud', string='Solicitud', required=True, index=True, ondelete='cascade')

    dtFechaCambioHistorial = fields.Datetime(string='Fecha del cambio', required=True, default=fields.Datetime.now)
    sMotivo = fields.Text(string='Motivo', required=True, help='Rellene el motivo del cambio de estado')
    sEstado = fields.Selection([
        ('recibida', 'Recibida'),
        ('preseleccionado', 'Preseleccionado'),
        ('aceptado', 'Aceptado'),
    ], string='Estado', required=True, default='recibida')
    name = fields.Char(string='Historial', compute='_compute_historial', store=True)

    bEstadoFinal = fields.Boolean(string='Estado final alcanzado', compute='_compute_estado_final', store=True)
    iLongitudMotivo = fields.Integer(string='Caracteres del motivo', compute='_compute_longitud_motivo', store=True)



    @api.constrains('sMotivo')
    def validar_motivo(self):
        for puntero in self:
            motivo = (puntero.sMotivo or '').strip()
            if not motivo:
                raise ValidationError('El motivo no puede estar en blanco')
            if len(motivo) > 240:
                raise ValidationError('El motivo no puede superar los 240 caracteres')

 
    @api.constrains('sMotivo')
    def validar_motivo_minimo(self):
        for puntero in self:
            motivo = (puntero.sMotivo or '').strip()
            if motivo and len(motivo) < 5:
                raise ValidationError('El motivo del cambio debe estar detallado con al menos 5 caracteres')


    @api.constrains('dtFechaCambioHistorial')
    def validar_fecha_cambio(self):
        for puntero in self:
            if puntero.dtFechaCambioHistorial > fields.Datetime.now():
                raise ValidationError('La fecha del cambio no puede ser futura')


    @api.constrains('solicitud_id', 'dtFechaCambioHistorial')
    def validar_historial_unico(self):
        for puntero in self:
            historial_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('solicitud_id', '=', puntero.solicitud_id.id),
                ('dtFechaCambioHistorial', '=', puntero.dtFechaCambioHistorial),
            ])
            if historial_repe:
                raise ValidationError('Esta solicitud ya tiene un cambio registrado en esa fecha y hora')

    @api.constrains('solicitud_id', 'sEstado')
    def validar_estado_no_repetido(self):
        for puntero in self:
            estado_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('solicitud_id', '=', puntero.solicitud_id.id),
                ('sEstado', '=', puntero.sEstado),
            ])
            if estado_repe:
                raise ValidationError('Esta solicitud ya tiene registrado un cambio a ese mismo estado en su historial')

    @api.depends('solicitud_id', 'dtFechaCambioHistorial')
    def _compute_historial(self):
        for puntero in self:
            puntero.sHistorial = '%s - %s' % (puntero.solicitud_id.display_name or '', puntero.dtFechaCambioHistorial or '')


    @api.depends('sEstado')
    def _compute_estado_final(self):
        for puntero in self:
            puntero.bEstadoFinal = (puntero.sEstado == 'aceptado')


    @api.depends('sMotivo')
    def _compute_longitud_motivo(self):
        for puntero in self:
            puntero.iLongitudMotivo = len((puntero.sMotivo or '').strip())

    @api.onchange('sMotivo')
    def _onchange_limpiar_motivo(self):
        for puntero in self:
            if puntero.sMotivo:
                puntero.sMotivo = puntero.sMotivo.strip()


    def unlink(self):
        for puntero in self:
            if puntero.sEstado == 'aceptado':
                raise ValidationError('Por motivos de auditoría, no se puede eliminar un registro de historial con estado Aceptado')
        return super(Historial, self).unlink()