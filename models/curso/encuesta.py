# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Encuesta(models.Model):

    _name = 'rrhh_upo.encuesta'
    _description = 'Encuesta de satisfacción con el profesorado'


    alumno_id = fields.Many2one('rrhh_upo.alumno', string='Alumno', required=True, index=True, ondelete='cascade')
    pdi_id = fields.Many2one('rrhh_upo.pdi', string='Profesor valorado', required=True, index=True, ondelete='restrict')
    sCursoAcademico = fields.Char(string='Curso académico', required=True, help='Formato AAAA/AAAA, por ejemplo 2025/2026')
    iResultado = fields.Integer(string='Resultado', required=True, help='Satisfacción con el profesor, de 1 (muy insatisfecho) a 5 (muy satisfecho)')
    name = fields.Char(string='Encuesta', compute='_compute_encuesta', store=True)

    @api.constrains('sCursoAcademico')
    def validar_formato_curso_academico(self):
        for puntero in self:
            curso = (puntero.sCursoAcademico or '').strip()
            if not curso:
                raise ValidationError('El curso académico no puede estar en blanco')
            if not re.match(r'^[0-9]{4}/[0-9]{4}$', curso):
                raise ValidationError('El curso académico debe tener el formato AAAA/AAAA, por ejemplo 2025/2026')

    @api.constrains('sCursoAcademico')
    def validar_anios_curso_academico(self):
        for puntero in self:
            curso = (puntero.sCursoAcademico or '').strip()
            if re.match(r'^[0-9]{4}/[0-9]{4}$', curso):
                anio_inicio, anio_fin = curso.split('/')
                if int(anio_fin) != int(anio_inicio) + 1:
                    raise ValidationError('El segundo año del curso académico debe ser el siguiente al primero')
                if int(anio_inicio) < 1997 or int(anio_inicio) > 2100:
                    raise ValidationError('El año de inicio del curso académico debe estar comprendido entre 1997 y 2100')

    @api.constrains('iResultado')
    def validar_resultado(self):
        for puntero in self:
            if puntero.iResultado < 1 or puntero.iResultado > 5:
                raise ValidationError('El resultado tiene que estar entre 1 y 5')

    @api.constrains('alumno_id', 'pdi_id', 'sCursoAcademico')
    def validar_encuesta_unica(self):
        for puntero in self:
            encuesta_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('alumno_id', '=', puntero.alumno_id.id),
                ('pdi_id', '=', puntero.pdi_id.id),
                ('sCursoAcademico', '=', (puntero.sCursoAcademico or '').strip()),
            ])
            if encuesta_repe:
                raise ValidationError('Este alumno ya ha valorado a este profesor en ese curso académico')

    @api.constrains('alumno_id', 'sCursoAcademico')
    def validar_limite_encuestas_alumno(self):
        for puntero in self:
            total_encuestas = self.search_count([
                ('alumno_id', '=', puntero.alumno_id.id),
                ('sCursoAcademico', '=', (puntero.sCursoAcademico or '').strip()),
            ])
            if total_encuestas > 12:
                raise ValidationError('Un alumno no puede registrar más de 12 encuestas en un mismo curso académico')

    @api.depends('alumno_id', 'pdi_id', 'sCursoAcademico')
    def _compute_encuesta(self):
        for puntero in self:
            puntero.name = '%s - %s - %s' % (
                puntero.alumno_id.display_name or '',
                puntero.pdi_id.display_name or '',
                puntero.sCursoAcademico or '',
            )

    @api.onchange('sCursoAcademico')
    def _onchange_curso(self):
        for puntero in self:
            if puntero.sCursoAcademico:
                puntero.sCursoAcademico = puntero.sCursoAcademico.strip()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sCursoAcademico'):
                vals['sCursoAcademico'] = vals['sCursoAcademico'].strip()
        return super(Encuesta, self).create(vals_list)