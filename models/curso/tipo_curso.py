# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tipo_curso(models.Model):

    _name = 'rrhh_upo.tipo_curso'
    _description = 'Tipo de curso'

    curso_ids = fields.One2many('rrhh_upo.curso', 'tipoCurso_id', string='Cursos')

    name = fields.Char(string='Nombre', required=True, help='Rellene el nombre del tipo de curso')
    sDescripcion = fields.Char(string='Descripcion', help='Rellene la descripcion del tipo de curso (opcional)')

    iNumCursos = fields.Integer(string='Nº de cursos asociados', compute='_compute_num_cursos', store=True)
    fTotalHorasCursos = fields.Float(string='Total horas ofertadas', compute='_compute_total_horas_cursos', digits=(10, 2), store=True)


    @api.constrains('name')
    def validar_tipo(self):
        for puntero in self:
            tipo = (puntero.name or '').strip()
            if not tipo:
                raise ValidationError('El tipo de curso no puede estar en blanco')
            if len(tipo) > 20:
                raise ValidationError('El tipo de curso no puede superar los 20 caracteres')

    @api.constrains('name')
    def validar_tipo_minimo(self):
        for puntero in self:
            tipo = (puntero.name or '').strip()
            if tipo and len(tipo) < 3:
                raise ValidationError('El nombre del tipo de curso debe tener al menos 3 caracteres')

    @api.constrains('name')
    def validar_tipo_unico(self):
        for puntero in self:
            tipo = (puntero.name or '').strip()
            if tipo:
                tipo_repe = self.search_count([
                    ('id', '!=', puntero.id),
                    ('name', '=ilike', tipo),
                ])
                if tipo_repe:
                    raise ValidationError('Ya existe un tipo de curso con el mismo nombre')

    @api.constrains('sDescripcion')
    def validar_descripcion(self):
        for puntero in self:
            if len(puntero.sDescripcion or '') > 240:
                raise ValidationError('La descripción no puede superar los 240 caracteres')

    @api.constrains('name', 'sDescripcion')
    def validar_contenido_descripcion(self):
        for puntero in self:
            if puntero.sDescripcion is not False and puntero.sDescripcion != '':
                desc = puntero.sDescripcion.strip()
                tipo = (puntero.name or '').strip()
                if not desc:
                    raise ValidationError('La descripción no puede estar formada únicamente por espacios en blanco')
                if desc.lower() == tipo.lower():
                    raise ValidationError('La descripción debe aportar más detalle y no ser idéntica al nombre del tipo de curso')


    @api.depends('curso_ids')
    def _compute_num_cursos(self):
        for puntero in self:
            puntero.iNumCursos = len(puntero.curso_ids)

    @api.depends('curso_ids.fEstimacionHoras')
    def _compute_total_horas_cursos(self):
        for puntero in self:
            puntero.fTotalHorasCursos = sum(curso.fEstimacionHoras for curso in puntero.curso_ids)

    @api.onchange('name', 'sDescripcion')
    def _onchange_limpiar_textos(self):
        for puntero in self:
            if puntero.name:
                puntero.name = puntero.name.strip()
            if puntero.sDescripcion:
                puntero.sDescripcion = puntero.sDescripcion.strip()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name'):
                vals['name'] = vals['name'].strip()
            if vals.get('sDescripcion'):
                vals['sDescripcion'] = vals['sDescripcion'].strip()
        return super(Tipo_curso, self).create(vals_list)
    
    def unlink(self):
        for puntero in self:
            if puntero.curso_ids:
                raise ValidationError('No se puede eliminar un tipo de curso que tiene cursos asociados')
        return super(Tipo_curso, self).unlink()