# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Experiencia_laboral(models.Model):

    _name = 'rrhh_upo.experiencia_laboral'
    _description = 'Experiencia laboral de la solicitud'

    solicitud_id = fields.Many2one('rrhh_upo.solicitud', string='Solicitud', required=True, index=True, ondelete='cascade')

    sNombreEmpresa = fields.Char(string='Empresa', required=True, help='Rellene el nombre de la empresa')
    sCargo = fields.Char(string='Cargo', required=True, help='Rellene el cargo desempeñado')
    dFechaInicioExperiencia = fields.Date(string='Fecha de inicio', required=True, default=fields.Date.today)
    dFechaFinExperiencia = fields.Date(string='Fecha de fin')
    name = fields.Char(string='Experiencia', compute='_compute_experiencia', store=True)
    bTrabajoActual = fields.Boolean(string='Trabajo actual', compute='_compute_trabajo_actual', store=True)
    iDiasTrabajados = fields.Integer(string='Días de experiencia', compute='_compute_dias_trabajados', store=True)


    @api.constrains('sNombreEmpresa')
    def validar_empresa(self):
        for puntero in self:
            empresa = (puntero.sNombreEmpresa or '').strip()
            if not empresa:
                raise ValidationError('El nombre de la empresa no puede estar en blanco')
            if len(empresa) > 50:
                raise ValidationError('El nombre de la empresa no puede superar los 50 caracteres')

    @api.constrains('sCargo')
    def validar_cargo(self):
        for puntero in self:
            cargo = (puntero.sCargo or '').strip()
            if not cargo:
                raise ValidationError('El cargo no puede estar en blanco')
            if len(cargo) > 50:
                raise ValidationError('El cargo no puede superar los 50 caracteres')

    @api.constrains('dFechaInicioExperiencia', 'dFechaFinExperiencia')
    def validar_fechas(self):
        for puntero in self:
            if puntero.dFechaInicioExperiencia > fields.Date.today():
                raise ValidationError('La fecha de inicio no puede ser futura')
            if puntero.dFechaFinExperiencia:
                if puntero.dFechaFinExperiencia <= puntero.dFechaInicioExperiencia:
                    raise ValidationError('La fecha de fin debe ser posterior a la de inicio')
                if puntero.dFechaFinExperiencia > fields.Date.today():
                    raise ValidationError('La fecha de fin no puede ser futura')

    @api.constrains('dFechaInicioExperiencia', 'dFechaFinExperiencia')
    def validar_antiguedad_maxima(self):
        for puntero in self:
            if puntero.dFechaInicioExperiencia and puntero.dFechaInicioExperiencia.year < 1950:
                raise ValidationError('El año de inicio de la experiencia laboral no puede ser anterior a 1950')
            if puntero.dFechaInicioExperiencia and puntero.dFechaFinExperiencia:
                dias = (puntero.dFechaFinExperiencia - puntero.dFechaInicioExperiencia).days
                if dias > 18250:
                    raise ValidationError('La duración de una misma experiencia laboral no puede superar los 50 años')

    @api.constrains('solicitud_id', 'sNombreEmpresa', 'sCargo', 'dFechaInicioExperiencia')
    def validar_experiencia_unica(self):
        for puntero in self:
            experiencia_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('solicitud_id', '=', puntero.solicitud_id.id),
                ('sNombreEmpresa', '=ilike', (puntero.sNombreEmpresa or '').strip()),
                ('sCargo', '=ilike', (puntero.sCargo or '').strip()),
                ('dFechaInicioExperiencia', '=', puntero.dFechaInicioExperiencia),
            ])
            if experiencia_repe:
                raise ValidationError('Esta solicitud ya tiene esa experiencia (misma empresa, cargo y fecha de inicio)')


    @api.depends('sNombreEmpresa', 'sCargo')
    def _compute_experiencia(self):
        for puntero in self:
            puntero.sExperiencia = '%s - %s' % (puntero.sNombreEmpresa or '', puntero.sCargo or '')

    @api.depends('dFechaFinExperiencia')
    def _compute_trabajo_actual(self):
        for puntero in self:
            puntero.bTrabajoActual = not bool(puntero.dFechaFinExperiencia)

    @api.depends('dFechaInicioExperiencia', 'dFechaFinExperiencia')
    def _compute_dias_trabajados(self):
        hoy = fields.Date.today()
        for puntero in self:
            if puntero.dFechaInicioExperiencia:
                fecha_fin = puntero.dFechaFinExperiencia or hoy
                if fecha_fin >= puntero.dFechaInicioExperiencia:
                    puntero.iDiasTrabajados = (fecha_fin - puntero.dFechaInicioExperiencia).days
                else:
                    puntero.iDiasTrabajados = 0
            else:
                puntero.iDiasTrabajados = 0

    @api.onchange('sNombreEmpresa', 'sCargo')
    def _onchange_limpiar_textos(self):
        for puntero in self:
            if puntero.sNombreEmpresa:
                puntero.sNombreEmpresa = puntero.sNombreEmpresa.strip()
            if puntero.sCargo:
                puntero.sCargo = puntero.sCargo.strip()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sNombreEmpresa'):
                vals['sNombreEmpresa'] = vals['sNombreEmpresa'].strip()
            if vals.get('sCargo'):
                vals['sCargo'] = vals['sCargo'].strip()
        return super(Experiencia_laboral, self).create(vals_list)