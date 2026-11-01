from odoo import models, fields, api

class Sala(models.Model):

    _name = 'RRHH_UPO.sala'
    _description = 'sala'

    name = fields.Char(string='Nombre',required=True, help='Dame el nombre de la sala')
    edificio =fields.Integer('Edificio')
    planta = fields.Integer('Planta')
    direccion = fields.Integer('Dirección')
    aforo = fields.Integer('Aforo')
    superficie = fields.Float('Superficie (m^2)')
    altura = fields.Float('Altura (m)')
    hora_apertura = fields.Datetime('Apertura', autodate = True)
    hora_cierre = fields.Datetime('Cierre', autodate = True)
    estado = fields.Selection([
        ('disponible','Disponible'),
        ('ocupada','Ocupada'),
        ('mantenimiento','Mantenimiento'),
    ],'Estado')

    
