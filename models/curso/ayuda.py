# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ayuda(models.Model):

    _name = 'rrhh_upo.ayuda'
    _description = 'Ayuda solicitada por un alumno'

    tipoAyuda_id = fields.Many2one('rrhh_upo.tipo_ayuda', string='Tipo de ayuda', required=True, index=True, ondelete='restrict')
    alumno_id = fields.Many2one('rrhh_upo.alumno', string='Alumno solicitante', required=True, index=True, ondelete='restrict')
    personalRRHH_ids = fields.Many2many('rrhh_upo.personal_rrhh', 'rrhh_upo_ayuda_personal_rrhh_rel', 'ayuda_id', 'personal_id', string='Personal que administra')

    name = fields.Char(string='Nombre', required=True, help='Nombre de la ayuda')
    fImporte = fields.Float(string='Importe', required=True, digits=(10, 2), help='Importe de la ayuda en euros')

    iNumPersonal = fields.Integer(string='Nº de gestores RRHH', compute='_compute_num_personal', store=True)
    sResumenAyuda = fields.Char(string='Resumen de solicitud', compute='_compute_resumen_ayuda', store=True)


    @api.constrains('name')
    def validar_nombre(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            if not nombre:
                raise ValidationError('El nombre de la ayuda no puede estar en blanco')
            if len(nombre) < 3:
                raise ValidationError('El nombre de la ayuda debe tener al menos 3 caracteres')

    @api.constrains('fImporte')
    def validar_importe(self):
        for puntero in self:
            if puntero.fImporte <= 0:
                raise ValidationError('El importe de la ayuda debe ser mayor que 0 euros')

    @api.constrains('fImporte')
    def validar_importe_maximo(self):
        for puntero in self:
            if puntero.fImporte > 10000:
                raise ValidationError('El importe de una ayuda individual no puede superar los 10.000 euros')

    @api.constrains('personalRRHH_ids')
    def validar_personal(self):
        for puntero in self:
            if not puntero.personalRRHH_ids:
                raise ValidationError('La ayuda debe estar administrada por al menos un miembro del personal de RRHH')

    @api.constrains('alumno_id', 'tipoAyuda_id', 'name')
    def validar_ayuda_unica_alumno(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            ayuda_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('alumno_id', '=', puntero.alumno_id.id),
                ('tipoAyuda_id', '=', puntero.tipoAyuda_id.id),
                ('name', '=ilike', nombre),
            ])
            if ayuda_repe:
                raise ValidationError('Este alumno ya tiene registrada una solicitud para esta misma ayuda')


    @api.depends('personalRRHH_ids')
    def _compute_num_personal(self):
        for puntero in self:
            puntero.iNumPersonal = len(puntero.personalRRHH_ids)

    @api.depends('name', 'alumno_id', 'fImporte')
    def _compute_resumen_ayuda(self):
        for puntero in self:
            puntero.sResumenAyuda = '%s - %s (%.2f €)' % (
                puntero.name or '',
                puntero.alumno_id.display_name or '',
                puntero.fImporte or 0.0
            )

    @api.onchange('name', 'fImporte')
    def _onchange_formatear_datos(self):
        for puntero in self:
            if puntero.name:
                puntero.name = puntero.name.strip()
            if puntero.fImporte and puntero.fImporte < 0:
                puntero.fImporte = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name'):
                vals['name'] = vals['name'].strip()
        return super(Ayuda, self).create(vals_list)

    def unlink(self):
        for puntero in self:
            if puntero.fImporte > 3000:
                raise ValidationError('Por motivos de auditoría, no se puede eliminar una ayuda cuyo importe supere los 3.000 €')
        return super(Ayuda, self).unlink()