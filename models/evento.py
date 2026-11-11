# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Evento(models.Model):
    _name= 'rrhh_upo.evento'
    _description = 'Evento'
    _rec_name = 'name'

    #Autocalculado
    name = fields.Char(string='Identificador del Evento',compute='generar_identifcador_evento',store=True)
    sTitulo = fields.Char(string='Titulo del evento', size=30, required=True, help = 'Introduce el titulo del evento')
    dFechaInicio = fields.DateTime(string='Fecha de inicio', required=True, help="Introduce la fecha de inicio del evento")
    dFechaFin = fields.DateTime(string='Fecha de finalización', required=True, help="Introduce la fecha de finalización del evento")
    sDescripcion = fields.Text()
    sUbicacion = fields.Char(string='Ubicación del evento', size=30, required=True, help = 'Introduce la ubicación del evento')


    stand_ids = fields.One2many('rrhh_upo.stand','evento_id','Stand')

    _sql_constraints = [('Evento_unico', 'UNIQUE(name)', 'El evento debe ser único')]

    #Construyo un name unico a partir del titulo y la fecha de inicio
    @api.depends('sTitulo', 'dFechaInicio')
    def generar_identificador_evento(self):
        for record in self:
            if record.sTitulo and record.dFechaInicio:
                record.name = f'{record.sTitulo} - {record.dFechaInicio}'
            else:
                record.name = False

    @api.constrains('sTitulo')
    def validar_titulo(self):
        for record in self:
            if not record.sTitulo.strip():
                raise models.ValidationError('El título del evento no puede estar en blanco')

    @api.constrains('sUbicacion')
    def validar_ubicacion(self):
        for record in self:
            if not record.sUbicacion.strip():
                raise models.ValidationError('La ubicación no puede estar en blanco')

    @api.constrains('dFechaInicio', 'dFechaFin')
    def validar_fechas(self):
        for record in self:
            if record.dFechaInicio and record.dFechaFin:
                if record.dFechaFin <= record.dFechaInicio:
                    raise models.ValidationError('La fecha de finalización debe ser posterior a la fecha de inicio')

    @api.onchange('dFechaInicio', 'dFechaFin')
    def onchange_fechas(self):
        if self.dFechaInicio and self.dFechaFin:
            if self.dFechaFin <= self.dFechaInicio:
                return {
                'warning': {'title': 'Fechas incorrectas','message': 'La fecha de finalización debe ser posterior a la fecha de inicio'}
            }