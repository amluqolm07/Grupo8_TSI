# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Edificio(models.Model):

    _name = 'rrhh_upo.edificio'
    _description = 'Edificio del campus'

    salas_ids = fields.One2many('rrhh_upo.sala', 'm2oEdificio', string='Salas')
    departamentos_ids = fields.One2many('rrhh_upo.departamento', 'm2oEdificio', string='Departamentos')

    iNumero = fields.Integer(string='Número', required=True, index=True, help='Número identificativo del edificio, por ejemplo 22')
    sUbicacion = fields.Char(string='Ubicación', required=True, help='Ubicación del edificio dentro del campus')
    sTelefono = fields.Char(string='Teléfono', required=True, help='9 dígitos, por ejemplo 954349000')
    name = fields.Char(string='Edificio', compute='_compute_edificio', store=True)
    iNumSalas = fields.Integer(string='Número de salas', compute='_compute_num_salas', store=True)
    iNumDepartamentos = fields.Integer(string='Número de departamentos', compute='_compute_num_departamentos', store=True)

    @api.constrains('iNumero')
    def validar_numero(self):
        for puntero in self:
            if puntero.iNumero <= 0 or puntero.iNumero > 100:
                raise ValidationError('El número del edificio debe estar comprendido entre 1 y 100')

    @api.constrains('iNumero')
    def validar_numero_unico(self):
        for puntero in self:
            numero_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('iNumero', '=', puntero.iNumero),
            ])
            if numero_repe:
                raise ValidationError('Ya existe un edificio con ese número')

    @api.constrains('sUbicacion')
    def validar_ubicacion(self):
        for puntero in self:
            ubicacion = (puntero.sUbicacion or '').strip()
            if not ubicacion:
                raise ValidationError('La ubicación del edificio no puede estar en blanco')
            if len(ubicacion) < 3:
                raise ValidationError('La ubicación del edificio debe tener al menos 3 caracteres')

    @api.constrains('sTelefono')
    def validar_telefono(self):
        for puntero in self:
            telefono = (puntero.sTelefono or '').replace(' ', '')
            if not telefono:
                raise ValidationError('El teléfono no puede estar en blanco')
            if not re.match(r'^[6789][0-9]{8}$', telefono):
                raise ValidationError('El teléfono debe tener 9 dígitos válidos (empezando por 6, 7, 8 o 9), por ejemplo 954349000')

    @api.constrains('sTelefono')
    def validar_telefono_unico(self):
        for puntero in self:
            telefono = (puntero.sTelefono or '').replace(' ', '')
            if telefono:
                telefono_repe = self.search_count([
                    ('id', '!=', puntero.id),
                    ('sTelefono', '=', telefono),
                ])
                if telefono_repe:
                    raise ValidationError('Ese número de teléfono ya está asignado a otro edificio del campus')

    @api.depends('iNumero')
    def _compute_edificio(self):
        for puntero in self:
            puntero.sEdificio = 'Edificio %s' % puntero.iNumero

    @api.depends('salas_ids')
    def _compute_num_salas(self):
        for puntero in self:
            puntero.iNumSalas = len(puntero.salas_ids)

    @api.depends('departamentos_ids')
    def _compute_num_departamentos(self):
        for puntero in self:
            puntero.iNumDepartamentos = len(puntero.departamentos_ids)

    @api.onchange('sUbicacion', 'sTelefono')
    def _onchange_limpiar_campos(self):
        for puntero in self:
            if puntero.sUbicacion:
                puntero.sUbicacion = puntero.sUbicacion.strip()
            if puntero.sTelefono:
                puntero.sTelefono = puntero.sTelefono.replace(' ', '').strip()

    def unlink(self):
        for puntero in self:
            if puntero.salas_ids or puntero.departamentos_ids:
                raise ValidationError('No se puede eliminar un edificio que tiene salas o departamentos asociados')
        return super(Edificio, self).unlink()


   