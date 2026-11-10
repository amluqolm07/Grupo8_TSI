# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Parte_horario(models.Model):
    _name = 'rrhh_upo.parte_horario'
    _description = 'Parte horario'
    
    name = fields.Char(string='id', size=7, required=True, help='Rellene el id del parte horario (7 carácteres)')
    dFecha_hora_entrada = fields.Datetime('Fecha y hora de entrada')
    sMetodo_validacion= fields.Selection([
        ('firma digital','Firma digital'),
        ('firma biometrica','Firma biométrica'),
        ('firma manuscrita','Firma manuscrita'),
    ],'Método de validación',required=True)
    bValidado = fields.Boolean('Validado',default=False)
    dFecha_hora_salida = fields.Datetime('Fecha y hora de la salida')
    sIncidencias = fields.Text('Incidencias/Justificaciones',size=240)

    fHoras_trabajadas = fields.Float('Horas trabajadas',compute='calcular_horas_trabajadas', stored=True)

    empleado_id = fields.Many2one('rrhh_upo.empleado',String='Empleado')
    ausencia_id = fields.One2many('rrhh_upo.ausencia',string='Ausencia')
    contrato_id = fields.Many2one('rrhh_upo.contrato',string='Contrato')

    _sql_constraints = [('Parte_horario_unico', 'unique(name)', 'El id del parte horario debe ser unico')]

    #Horas trabajadas = salida-entrada (segundos a horas)
    @api.depends('dFecha_hora_entrada','dFecha_hora_salida')
    def _calcular_horas_trabajadas(self):
        for record in self:
            if record.dFecha_hora_entrada and record.dFecha_hora_salida:
                diferencia = record.dFecha_hora_salida - record.dFecha_hora_entrada
                record.fHoras_trabajadas = diferencia.total_seconds() / 3600.0
            else:
                record.fHoras_trabajadas = 0

    #No se pude salir antes de entrar
    @api.constrains('dFecha_hora_entrada', 'dFecha_hora_salida')
    def _check_fechas_horario(self):
        for record in self:
            if record.dFecha_hora_salida and record.dFecha_hora_entrada and record.dFecha_hora_salida < record.dFecha_hora_entrada:
                raise ValidationError('La fecha y hora de salida no puede ser anterior a la de entrada')

   