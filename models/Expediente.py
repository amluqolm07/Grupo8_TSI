# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Expediente(models.Model):
    
    _name = 'rrhh_upo.expediente'
    _description = 'Expediente'
    
    name = fields.Date(string='Fecha_apertura', help = "Fecha de apertura del expediente", required=True)
    fecha_fin = fields.Date('Fecha de cierre')
    estado = fields.Selection([('abierto', 'Abierto'), 
                               ('cerrado', 'Cerrado')], 'Estado', default='abierto', required=True)
    
    nota_media = fields.Float('Nota media', compute='_compute_nota_media', store=True, aggregator='avg')
    creditos_superados = fields.Integer('Créditos superados' , compute='_compute_creditos_superados', store=True)
    
    
    grado_id = fields.Many2one('rrhh_upo.grado', string='Grado', required=True)
    
    matricula_ids = fields.One2many('rrhh_upo.matricula', 'expediente_id', 'Matrículas del expediente')
    
    _sql_constraints = [('rrhh_upo_expediente_name_unique', 'UNIQUE(name)', 'La fecha de apertura del expediente debe ser única.')]
    
    
    @api.depends('matricula_ids.nota')
    def _compute_nota_media(self):
        for expediente in self:
            notas = expediente.matricula_ids.mapped('matricula_contiene_asignatura_ids.nota')
            expediente.nota_media = sum(notas) / len(notas) if notas else 0.0
            
    @api.depends('matricula_ids.asignatura_id.creditos', 'matricula_ids.matricula_contiene_asignatura_ids.nota')
    def _compute_creditos_superados(self):
        for expediente in self:
            creditos = [asignatura.creditos for matricula in expediente.matricula_ids for asignatura in matricula.asignatura_id if asignatura.creditos is not None]
            expediente.creditos_superados = sum(creditos)



    @api.constrains('name', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_fin and record.fecha_fin < record.name:
                raise models.ValidationError('La fecha de cierre no puede ser anterior a la de apertura.')

    @api.constrains('estado', 'fecha_fin')
    def _check_cerrado(self):
        for record in self:
            if record.estado != 'abierto' and not record.fecha_fin:
                raise models.ValidationError('Un expediente cerrado debe tener fecha de cierre.')

    def btn_submit_to_abierto(self):
        self.write({'estado': 'abierto'})

    def btn_submit_to_cerrado(self):
        self.write({'estado': 'cerrado'})