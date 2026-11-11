# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Inscripcion_curso(models.Model):

    _name = 'rrhh_upo.inscripcion_curso'
    _description = 'Inscripcion del curso'

    curso_id = fields.Many2one('rrhh_upo.curso', string='Curso', required=True, index=True, ondelete='cascade')
    empleado_id = fields.Many2one('rrhh_upo.empleado', string='Empleado', required=True, index=True, ondelete='cascade')
    prueba_ids = fields.One2many('rrhh_upo.prueba', 'inscripcionCurso_id', string='Pruebas')

    dFechaInscripcion = fields.Date(string='Fecha de inscripcion', required=True, default=fields.Date.today)
    dFechaFin = fields.Date(string='Fecha final del curso')
    sEstado = fields.Selection([
        ('recibida', 'Recibida'),
        ('preseleccionado', 'Preseleccionado'),
        ('aceptado', 'Aceptado'),
    ], string='Estado', required=True, default='recibida', help='Estado de la inscripción')
    name = fields.Char(string='Inscripción', compute='_compute_inscripcion', store=True)

    iNumPruebas = fields.Integer(string='Nº de pruebas', compute='_compute_num_pruebas', store=True)
    iDiasDuracion = fields.Integer(string='Duración (días)', compute='_compute_dias_duracion', store=True)


    @api.constrains('dFechaInscripcion', 'dFechaFin')
    def validar_fechas(self):
        for puntero in self:
            if puntero.dFechaFin and puntero.dFechaFin <= puntero.dFechaInscripcion:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inscripción')


    @api.constrains('dFechaInscripcion')
    def validar_fecha_inscripcion(self):
        for puntero in self:
            if puntero.dFechaInscripcion:
                if puntero.dFechaInscripcion > fields.Date.today():
                    raise ValidationError('La fecha de inscripción no puede ser posterior al día de hoy')
                if puntero.dFechaInscripcion.year < 1997:
                    raise ValidationError('El año de la fecha de inscripción no puede ser anterior a 1997')


    @api.constrains('empleado_id', 'curso_id', 'dFechaInscripcion')
    def validar_inscripcion_unica(self):
        for puntero in self:
            inscripcion_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('empleado_id', '=', puntero.empleado_id.id),
                ('curso_id', '=', puntero.curso_id.id),
                ('dFechaInscripcion', '=', puntero.dFechaInscripcion),
            ])
            if inscripcion_repe:
                raise ValidationError('Este empleado ya tiene una inscripción a este curso en esa fecha')


    @api.constrains('sEstado', 'dFechaFin')
    def validar_estado(self):
        for puntero in self:
            if puntero.sEstado == 'aceptado' and not puntero.dFechaFin:
                raise ValidationError('Una inscripción aceptada necesita fecha de fin')


    @api.constrains('prueba_ids')
    def validar_cupo_pruebas(self):
        for puntero in self:
            if len(puntero.prueba_ids) > 10:
                raise ValidationError('Una inscripción no puede superar el límite máximo de 10 pruebas asociadas')



    @api.depends('empleado_id', 'curso_id')
    def _compute_inscripcion(self):
        for puntero in self:
            puntero.sInscripcion = '%s - %s' % (puntero.empleado_id.display_name or '', puntero.curso_id.display_name or '')

    @api.depends('prueba_ids')
    def _compute_num_pruebas(self):
        for puntero in self:
            puntero.iNumPruebas = len(puntero.prueba_ids)

    @api.depends('dFechaInscripcion', 'dFechaFin')
    def _compute_dias_duracion(self):
        for puntero in self:
            if puntero.dFechaInscripcion and puntero.dFechaFin and puntero.dFechaFin > puntero.dFechaInscripcion:
                puntero.iDiasDuracion = (puntero.dFechaFin - puntero.dFechaInscripcion).days
            else:
                puntero.iDiasDuracion = 0

    @api.onchange('sEstado', 'dFechaInscripcion')
    def _onchange_estado_fecha_fin(self):
        for puntero in self:
            if puntero.sEstado == 'aceptado' and not puntero.dFechaFin:
                fecha_base = puntero.dFechaInscripcion or fields.Date.today()
                puntero.dFechaFin = fecha_base + timedelta(days=30)

    def unlink(self):
        for puntero in self:
            if puntero.prueba_ids or puntero.sEstado == 'aceptado':
                raise ValidationError('No se puede eliminar una inscripción aceptada o que ya tiene pruebas registradas')
        return super(Inscripcion_curso, self).unlink()