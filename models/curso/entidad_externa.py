# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Entidad_externa(models.Model):

    _name = 'rrhh_upo.entidad_externa'
    _description = 'Entidad externa'

    empleadosExternos_ids = fields.One2many('rrhh_upo.empleado_externo', 'm2oEntidadExterna', string='Empleados externos')
    financiaciones_ids = fields.One2many('rrhh_upo.financiacion', 'm2oEntidadExterna', string='Financiaciones')

    sCif = fields.Char(string='CIF', required=True, help='Rellene el CIF de la entidad (una letra, 7 números y un dígito o letra de control)')
    name = fields.Char(string='Nombre', required=True, help='Rellene el nombre de la entidad')
    sDireccion = fields.Char(string='Dirección', required=True, help='Rellene la dirección de la entidad')
    sTelefono = fields.Char(string='Teléfono', help='Rellene el teléfono de la entidad (9 dígitos)')
    iNumEmpleados = fields.Integer(string='Nº de empleados externos', compute='_compute_num_empleados', store=True)
    iNumFinanciaciones = fields.Integer(string='Nº de financiaciones', compute='_compute_num_financiaciones', store=True)


    @api.constrains('sCif')
    def validar_cif(self):
        for puntero in self:
            cif = (puntero.sCif or '').strip().upper()
            if not cif:
                raise ValidationError('El CIF no puede estar en blanco')
            if not re.match(r'^[A-Z][0-9]{7}[0-9A-J]$', cif):
                raise ValidationError('El CIF debe tener una letra, 7 números y un dígito o letra de control')
            cif_repe = self.search_count([
                ('id', '!=', puntero.id),
                ('sCif', '=ilike', cif),
            ])
            if cif_repe:
                raise ValidationError('Ya existe una entidad externa con el mismo CIF')

    @api.constrains('name')
    def validar_nombre(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            if not nombre:
                raise ValidationError('El nombre no puede estar en blanco')
            if len(nombre) > 50:
                raise ValidationError('El nombre no puede superar los 50 caracteres')

    @api.constrains('name')
    def validar_nombre_unico(self):
        for puntero in self:
            nombre = (puntero.name or '').strip()
            if nombre:
                nombre_repe = self.search_count([
                    ('id', '!=', puntero.id),
                    ('name', '=ilike', nombre),
                ])
                if nombre_repe:
                    raise ValidationError('Ya existe una entidad externa registrada con el mismo nombre')

    @api.constrains('sDireccion')
    def validar_direccion(self):
        for puntero in self:
            direccion = (puntero.sDireccion or '').strip()
            if not direccion:
                raise ValidationError('La dirección no puede estar en blanco')
            if len(direccion) > 100:
                raise ValidationError('La dirección no puede superar los 100 caracteres')

    @api.constrains('sTelefono')
    def validar_telefono(self):
        for puntero in self:
            if puntero.sTelefono:
                telefono = puntero.sTelefono.replace(' ', '')
                if not re.match(r'^[0-9]{9}$', telefono):
                    raise ValidationError('El teléfono debe tener 9 dígitos')

    @api.depends('empleadosExternos_ids')
    def _compute_num_empleados(self):
        for puntero in self:
            puntero.iNumEmpleados = len(puntero.empleadosExternos_ids)

    @api.depends('financiaciones_ids')
    def _compute_num_financiaciones(self):
        for puntero in self:
            puntero.iNumFinanciaciones = len(puntero.financiaciones_ids)

    @api.onchange('sCif', 'name', 'sDireccion', 'sTelefono')
    def _onchange_formatear_datos(self):
        for puntero in self:
            if puntero.sCif:
                puntero.sCif = puntero.sCif.strip().upper()
            if puntero.name:
                puntero.name = puntero.name.strip()
            if puntero.sDireccion:
                puntero.sDireccion = puntero.sDireccion.strip()
            if puntero.sTelefono:
                puntero.sTelefono = puntero.sTelefono.replace(' ', '').strip()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sCif'):
                vals['sCif'] = vals['sCif'].strip().upper()
            if vals.get('name'):
                vals['name'] = vals['name'].strip()
        return super(Entidad_externa, self).create(vals_list)

    def unlink(self):
        for puntero in self:
            if puntero.empleadosExternos_ids or puntero.financiaciones_ids:
                raise ValidationError('No se puede eliminar una entidad externa que tiene empleados externos o financiaciones asociadas')
        return super(Entidad_externa, self).unlink()