# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OfertaEmpleo(models.Model):
    _name='rrhh_upo.oferta_empleo'
    _description = 'Oferta de empleo'
    _rec_name = 'sNombrePuesto'


    sReferenciaOferta = fields.Char(string='Referencia', size=10, required=True, help='Introduce una referencia identificativa para la oferta')
    sNombrePuesto = fields.Char(string='Nombre del puesto', size=20, required=True, help = 'Introduce el nombre del puesto de trabajo')
    sDescripcion = fields.text()
    dFechaPublicacion = fields.DateTime(string='Fecha de publicación', required=True, help='Introduce la fecha de publicación de la oferta de empleo')
    dFechaLimite = fields.DateTime(string='Fecha de limite', required=True, help='Introduce la fecha limite para aplicar a la oferta de empleo')
    iVacantes = fields.Integer(string='Número de vacantes', require=True,help='Introduce el número de vacantes disponible para la oferta de empleo')
    #True = "Publicada", por defecto la oferta esta en False = "Borrador"
    bPublicada = fields.Boolean(string='Publicada', default=False)

    requisito_ids = fields.One2many('rrhh_upo.requisito','Requisito')
    solicitud_ids = fields.One2many('rrhh_upo.solicitud','Solicitudes')
    material_ids = fields.One2many('rrhh_upo.material','Materiales')
    jornada_id = fields.Many2one('rrhh_upo.jornada','Jornada',required=True)
    

    _sql_constraints =[('oferta_unica','UNIQUE(sReferenciaOferta)','Ya existe una oferta con esa referencia')]






    