# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OfertaEmpleo(models.Model):
    _name='rrhh_upo.oferta_empleo'
    _description = 'Oferta de empleo'
    _rec_name = 'name'


    name = fields.Char(string='Referencia', size=10, required=True, help='Introduce una referencia identificativa para la oferta')
    sNombrePuesto = fields.Char(string='Nombre del puesto', size=20, required=True, help = 'Introduce el nombre del puesto de trabajo')
    sDescripcion = fields.Text()
    dFechaPublicacion = fields.DateTime(string='Fecha de publicación', required=True, help='Introduce la fecha de publicación de la oferta de empleo')
    dFechaLimite = fields.DateTime(string='Fecha de limite', required=True, help='Introduce la fecha limite para aplicar a la oferta de empleo')
    iVacantes = fields.Integer(string='Número de vacantes', required=True,help='Introduce el número de vacantes disponible para la oferta de empleo')
    #True = "Publicada", por defecto la oferta esta en False = "Borrador"
    bPublicada = fields.Boolean(string='Publicada', default=False)

    requisito_ids = fields.One2many('rrhh_upo.requisito','oferta_id','Requisito')
    solicitud_ids = fields.One2many('rrhh_upo.solicitud','oferta_id','Solicitudes')
    material_ids = fields.One2many('rrhh_upo.material','oferta_id','Materiales')
    jornada_ids = fields.One2many('rrhh_upo.jornada','oferta_empleo_id','Jornada')
    

    _sql_constraints =[('oferta_unica','UNIQUE(name)','Ya existe una oferta con esa referencia')]


    @api.constrains('name')
    def validar_referencia(self):
        for record in self:
            if not record.name.strip():
                raise models.ValidationError('La referencia no puede estar en blanco')

    @api.constrains('sNombrePuesto')
    def validar_nombre_puesto(self):
        for record in self:
            if not record.sNombrePuesto.strip():
                raise models.ValidationError('El nombre del puesto no puede estar en blanco')

    @api.constrains('iVacantes')
    def validar_vacantes(self):
        for record in self:
            if record.iVacantes <= 0:
                raise models.ValidationError('El número de vacantes debe ser mayor que 0')

    @api.constrains('dFechaPublicacion', 'dFechaLimite')
    def validar_fechas(self):
        for record in self:
            if record.dFechaLimite <= record.dFechaPublicacion:
                raise models.ValidationError('La fecha límite debe ser posterior a la fecha de publicación')

    @api.onchange('dFechaPublicacion', 'dFechaLimite')
    def onchange_fechas(self):
        if self.dFechaLimite and self.dFechaPublicacion:
            if self.dFechaLimite <= self.dFechaPublicacion:
             return {
                'warning': {'title': 'Fechas incorrectas','message': 'La fecha límite debe ser posterior a la fecha de publicación'}
            }




    