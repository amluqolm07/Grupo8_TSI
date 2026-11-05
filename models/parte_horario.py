# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Parte_horario(models.Model):
    _name = 'rrhh_upo.parte.horario'
    _description = 'Parte horario'
    _rec_name='fecha_hora_entrada'

    fecha_hora_entrada = fields.Datetime(name='Fecha y hora de entrada',required=True,help='Fecha y hora en la que entró al puesto')
    metodo_validacion= fields.Selection([
        ('firma digital','Firma digital'),
        ('firma biometrica','Firma biométrica'),
        ('firma manuscrita','Firma manuscrita'),
    ],'Método de validación',required=True)
    validado = fields.Boolean('Validado',default=False)
    fecha_hora_salida = fields.Datetime('Fecha y hora de la salida')
    incidencias = fields.Text('Incidencias/Justificaciones',size=240)

    horas_trabajadas = fields.Float('Horas trabajadas',compute='calcular_horas_trabajadas')

    #Horas trabajadas = salida-entrada (segundos a horas)
    @api.depends('fecha_hora_entrada','fecha_hora_salida')
    def calcular_horas_trabajadas(self):
        for record in self:
            if record.fecha_hora_entrada and record.fecha_hora_salida:
                diferencia = record.fecha_hora_salida - record.fecha_hora_entrada
                record.horas_trabajadas = diferencia.total_seconds() / 3600.0
            else:
                record.horas_trabajadas = 0

    #No se pude salir antes de entrar
    @api.constrains('fecha_hora_entrada', 'fecha_hora_salida')
    def _check_fechas_horario(self):
        for record in self:
            if record.fecha_hora_salida and record.fecha_hora_entrada and record.fecha_hora_salida < record.fecha_hora_entrada:
                raise ValidationError('La fecha y hora de salida no puede ser anterior a la de entrada')