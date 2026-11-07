# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Stand(models.Model):
    _name= 'rrhh_upo.stand'
    _description = 'Stand'
    _rec_name = 'name'

    #Autocalculado
    name = fields.Char(string='Identificador del Stand',compute='generar_nombre_stand',store=True)
    sNombreStand = fields.Char(string='Nombre del Stand', size=30, required=True, help = 'Introduce el nombre del Stand')
    sDescripcion = fields.Text()
    sCalle = fields.Char(string='Calle del Stand', size=30, required=True, help = 'Introduce la calle del Stand')
    iNumero = fields.Integer(string='Numero de la calle', size=4, required=True, help = 'Introduce el número del Stand')



    solicitud_ids = fields.One2many('rrhh_upo.solicitud','stand_id', 'Solicitud')
    evento_id = fields.Many2one('rrhh_upo.evento', 'Evento', required=True)


    _sql_constraints = [('Stand_unico', 'UNIQUE(name)', 'El Stand debe ser único y ya existe uno con ese numero y en esa calle')]

    #Combino las dos PK para formar name
    @api.depends('sCalle', 'iNumero')
    def generar_nombre_stand(self):
        for record in self:
            if record.sCalle and record.iNumero:
                record.name = f'{record.sCalle} - {record.iNumero}'
            else:
                record.name = False

    @api.constrains('sNombreStand')
    def validar_nombre(self):
        for record in self:
            if not record.sNombreStand.strip():
                raise models.ValidationError('El nombre del Stand no puede estar en blanco')

    @api.constrains('sCalle')
    def validar_calle(self):
        for record in self:
            if not record.sCalle.strip():
                raise models.ValidationError('La calle no puede estar en blanco')

    @api.constrains('iNumero')
    def validar_numero(self):
        for record in self:
            if record.iNumero <= 0:
                raise models.ValidationError('El número de la calle debe ser mayor que 0')