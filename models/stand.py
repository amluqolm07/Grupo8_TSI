# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Stand(models.Model):
    _name= 'rrhh_upo.stand'
    _description = 'Stand'
    _rec_name = 'sNombreStand'


    sNombreStand = fields.Char(string='Nombre del Stand', size=30, required=True, help = 'Introduce el nombre del Stand')
    sDescripcion = fields.text()
    sCalle = fields.Char(string='Calle del Stand', size=30, required=True, help = 'Introduce la calle del Stand')
    iNumero = fields.Integer(string='Numero de la calle', size=4, required=True, help = 'Introduce el número del Stand')



    solicitud_ids = fields.One2Many('rrhh_upo.solicitud', 'Solicitud')
    evento_id = fields.Many2one('rrhh_upo.evento', 'Evento', required=True)


    _sql_constraints = [('Stand_unico', 'UNIQUE(sCalle,iNumero)', 'El Stand debe ser único y ya existe uno con ese numero y en esa calle')]



