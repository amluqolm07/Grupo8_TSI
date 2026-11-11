# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Prueba(models.Model):

    _name = 'rrhh_upo.prueba'
    _description = 'Prueba'

    inscripcionCurso_id = fields.Many2one('rrhh_upo.inscripcion_curso', string='Inscripción', required=True, index=True, ondelete='cascade')

    name = fields.Char(string='Nombre', required=True, help='Rellene el nombre de la prueba')
    dFechaRealizacion = fields.Date(string='Fecha de realización', required=True, default=fields.Date.today)
    sResultado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('superada', 'Superada'),
        ('no_superada', 'No superada'),
    ], string='Resultado', required=True, default='pendiente')

    sResumenPrueba = fields.Char(string='Resumen de la prueba', compute='_compute_resumen_prueba', store=True)
    bEvaluada = fields.Boolean(string='Prueba evaluada', compute='_compute_evaluada', store=True)


    @api.constrains('name')
    def validar_nombre(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            if not nombre:
                raise ValidationError('El nombre de la prueba no puede estar en blanco')
            if len(nombre) > 30:
                raise ValidationError('El nombre de la prueba no puede superar los 30 caracteres')

    @api.constrains('inscripcionCurso_id', 'dFechaRealizacion')
    def validar_prueba_unica(self):
        for puntero in self:
            prueba_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('inscripcionCurso_id', '=', puntero.inscripcionCurso_id.id),
                ('dFechaRealizacion', '=', puntero.dFechaRealizacion),
            ])
            if prueba_repe:
                raise ValidationError('Esta inscripción ya tiene una prueba en esa fecha')

    @api.constrains('inscripcionCurso_id', 'name')
    def validar_nombre_unico_inscripcion(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            if nombre:
                nombre_repe = self.search_count([
                    ('id', '!=', puntero.id),
                    ('inscripcionCurso_id', '=', puntero.inscripcionCurso_id.id),
                    ('name', '=ilike', nombre),
                ])
                if nombre_repe:
                    raise ValidationError('Esta inscripción ya tiene registrada una prueba con ese mismo nombre')

    @api.constrains('dFechaRealizacion', 'inscripcionCurso_id')
    def validar_fecha_realizacion(self):
        for puntero in self:
            inscripcion = puntero.inscripcionCurso_id
            if puntero.dFechaRealizacion < inscripcion.dFechaInscripcion:
                raise ValidationError('La prueba no puede ser anterior a la fecha de inscripción')
            if inscripcion.dFechaFin and puntero.dFechaRealizacion > inscripcion.dFechaFin:
                raise ValidationError('La prueba no puede ser posterior a la fecha de fin de la inscripción')

    @api.constrains('dFechaRealizacion', 'sResultado')
    def validar_resultado_fecha(self):
        for puntero in self:
            if puntero.dFechaRealizacion and puntero.dFechaRealizacion > fields.Date.today():
                if puntero.sResultado != 'pendiente':
                    raise ValidationError('Una prueba con fecha de realización futura debe tener el resultado en estado Pendiente')



    @api.depends('inscripcionCurso_id', 'name', 'sResultado')
    def _compute_resumen_prueba(self):
        for puntero in self:
            puntero.sResumenPrueba = '%s - %s (%s)' % (
                puntero.inscripcionCurso_id.display_name or '',
                puntero.name or '',
                puntero.sResultado or ''
            )

    @api.depends('sResultado')
    def _compute_evaluada(self):
        for puntero in self:
            puntero.bEvaluada = (puntero.sResultado in ['superada', 'no_superada'])

    @api.onchange('name', 'dFechaRealizacion')
    def _onchange_nombre_fecha(self):
        for puntero in self:
            if puntero.name:
                puntero.name = puntero.name.strip()
            if puntero.dFechaRealizacion and puntero.dFechaRealizacion > fields.Date.today():
                puntero.sResultado = 'pendiente'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name'):
                vals['name'] = vals['name'].strip()
        return super(Prueba, self).create(vals_list)

    def unlink(self):
        for puntero in self:
            if puntero.sResultado == 'superada':
                raise ValidationError('No se puede eliminar una prueba que ya figura como Superada')
        return super(Prueba, self).unlink()