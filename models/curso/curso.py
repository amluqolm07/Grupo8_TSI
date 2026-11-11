# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Curso(models.Model):
    _name = 'rrhh_upo.curso'
    _description = 'Curso'

    tipoCurso_id = fields.Many2one('rrhh_upo.tipo_curso', string='Tipo de curso', required=True, index=True, ondelete='restrict')
    inscripcionCurso_ids = fields.One2many('rrhh_upo.inscripcion_curso', 'curso_id', string='Inscripciones')
    ofertaEmpleo_id = fields.Many2one('rrhh_upo.oferta_empleo', string='Oferta de empleo', required=True, index=True, ondelete='restrict')

    name = fields.Char(string='Curso', required=True)
    fEstimacionHoras = fields.Float(string='Estimacion horas', required=True, digits=(10, 2))
    iNumInscritos = fields.Integer(string='Nº de inscritos', compute='_compute_num_inscritos', store=True)
    fCreditosEcts = fields.Float(string='Créditos ECTS equivalentes', compute='_compute_creditos_ects', digits=(6, 2), store=True)


    @api.constrains('name')
    def validar_curso(self):
        for puntero in self:
            curso = (puntero.name or '').strip()
            if not curso:
                raise ValidationError('El curso no puede estar en blanco')
            if len(curso) > 30:
                raise ValidationError('El curso no puede superar los 30 caracteres')

    @api.constrains('sCurso')
    def validar_curso_unico(self):
        for puntero in self:
            curso = (puntero.sCurso or '').strip()
            if curso:
                curso_repe = self.search_count([
                    ('id', '!=', puntero.id),
                    ('sCurso', '=ilike', curso),
                ])
                if curso_repe:
                    raise ValidationError('Ya existe un curso con el mismo nombre')

    @api.constrains('fEstimacionHoras')
    def validar_estimacion_horas(self):
        for puntero in self:
            if puntero.fEstimacionHoras <= 0:
                raise ValidationError('La estimacion de horas tiene que ser mayor que 0')
            if puntero.fEstimacionHoras > 1000:
                raise ValidationError('La estimacion de horas no puede superar las 1000 horas')

    @api.constrains('ofertaEmpleo_id')
    def validar_ofertaEmpleo_id(self):
        for puntero in self:
            curso_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('ofertaEmpleo_id', '=', puntero.ofertaEmpleo_id.id),
            ])
            if curso_repe:
                raise ValidationError('Esa oferta de empleo ya tiene un curso asignado')

    @api.constrains('inscripcionCurso_ids')
    def validar_cupo_inscripciones(self):
        for puntero in self:
            if len(puntero.inscripcionCurso_ids) > 50:
                raise ValidationError('El curso ha alcanzado el límite máximo de 50 inscripciones permitidas')


    @api.depends('inscripcionCurso_ids')
    def _compute_num_inscritos(self):
        for puntero in self:
            puntero.iNumInscritos = len(puntero.inscripcionCurso_ids)

    @api.depends('fEstimacionHoras')
    def _compute_creditos_ects(self):
        for puntero in self:
            if puntero.fEstimacionHoras > 0:
                puntero.fCreditosEcts = puntero.fEstimacionHoras / 25.0
            else:
                puntero.fCreditosEcts = 0.0

    @api.onchange('sCurso', 'fEstimacionHoras')
    def _onchange_curso_horas(self):
        for puntero in self:
            if puntero.sCurso:
                puntero.sCurso = puntero.sCurso.strip()
            if puntero.fEstimacionHoras and puntero.fEstimacionHoras < 0:
                puntero.fEstimacionHoras = 1.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sCurso'):
                vals['sCurso'] = vals['sCurso'].strip()
        return super(Curso, self).create(vals_list)


    def unlink(self):
        for puntero in self:
            if puntero.inscripcionCurso_ids:
                raise ValidationError('No se puede eliminar un curso que ya tiene inscripciones asociadas')
        return super(Curso, self).unlink()