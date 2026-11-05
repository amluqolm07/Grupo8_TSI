# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Evento(models.Model):
    _name= 'rrhh_upo.evento'
    _description = 'Evento'
    _rec_name = 'sTitulo'


    sTitulo = fields.Char(string='Titulo del evento', size=30, required=True, help = 'Introduce el titulo del evento')
    dFechaInicio = fields.DateTime(string='Fecha de inicio', required=True, help="Introduce la fecha de inicio del evento")
    dFechaFin = fields.DateTime(string='Fecha de finalización', required=True, help="Introduce la fecha de finalización del evento")
    sDescripcion = fields.text()
    sUbicacion = fields.Char(string='Ubicación del evento', size=30, required=True, help = 'Introduce la ubicación del evento')


    stand_ids = fields.One2many('rrhh_upo.stand','Stand')

    _sql_constraints = [('Evento_unico', 'UNIQUE(sTitulo,dFechaInicio)', 'El evento debe ser único, ya existe un evento con ese título y con esa fecha de inicio')]