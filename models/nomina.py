from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Nomina(models.Model):
    _name = 'rrhh_upo.nomina'
    _description = 'Nómina'

    #Relaciones de la nómina:

    m2oContrato = fields.Many2one('rrhh_upo.contrato', string='Contrato', required=True, index=True)
    o2mConceptos = fields.One2many('rrhh_upo.concepto', 'm2oNomina', string='Conceptos')

    #Declaración de los campos y validaciones básicas:

    #Validación: El usuario debe elegir una de esas opciones de forma obligatoria y no puede quedar vacio.
    sPeriodoMes = fields.Selection([
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
        ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
        ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
        ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),
    ], string='Mes', required=True)

    #Validación: El usuario debe introducir un número entero y no puede quedar vacio.
    iPeriodoAnio = fields.Integer(string='Año', required=True)

    #Validación: El usuario debe introducir un valor de tipo float y no puede quedar vacio, además se redondea a dos decimales.
    fSalarioBruto = fields.Float(string='Salario bruto', required=True, digits=(10, 2))

    #Validación: El usuario debe introducir una fecha valida y no puede quedar vacio.
    dFechaEmision = fields.Date(string='Fecha de emisión', required=True, default=fields.Date.today)

    #Validación: Campo autocalculado (no lo introduce el usuario). store=True para guardarlo en la BD.
    fTotalDeducciones = fields.Float(string='Total deducciones', compute='calcular_importe', store=True)

    #Validación: Campo autocalculado (no lo introduce el usuario), store=True para guardarlo en la BD.
    fSalarioNeto = fields.Float(string='Salario neto', compute='calcular_importe', store=True)

    #Validación: Solo admite booleanos True = "Emitida" y por defecto la nomina esta en False = "Borrador".
    bEmitida = fields.Boolean(string='Emitida', default=False)

    #Metodos con validaciones y cálculos:

    #Validación: Compruebo que tiene 4 cifras y que el periodo del año esta entre el año que se fundo la UPO (1997) y el año actual.
    @api.constrains('iPeriodoAnio')
    def validacion_periodo_anio(self):
        for nomina in self:
            if len(str(nomina.iPeriodoAnio)) != 4:
                raise ValidationError('El año debe tener 4 cifras')
            if not 1997 <= nomina.iPeriodoAnio <= date.today().year: 
                raise ValidationError(f'El año debe estar entre 1997 y {date.today().year}')
            
    #Validación: El salario bruto introducido debe ser mayor que 0.
    @api.constrains('fSalarioBruto')
    def validacion_salario_bruto(self):
        for nomina in self:
            if nomina.fSalarioBruto <= 0:
                raise ValidationError('El salario bruto tiene que ser mayor que 0')

    #Validación: Comprueba que la fecha de emisión no esta en el futuro.
    @api.constrains('dFechaEmision')
    def validacion_fecha_emision(self):
        for nomina in self:
            if nomina.dFechaEmision > date.today():
                raise ValidationError('La fecha de emisión no puede ser futura')

    #Cálculo:
    @api.depends('fSalarioBruto','o2mConceptos.fImporte','o2mConceptos.m2oTipoConcepto.bEsDeduccion')
    def calcular_importe(self):
        for record in self:
            #Deducciones va a ser el conjunto que necesitamos para hacer los cálculos del salario neto.
            deducciones = record.o2mConceptos.filtered(lambda concepto: concepto.m2oTipoConcepto.bEsDeduccion)
            #Extras van a ser conceptos que no son deducción, por tanto suman al salario neto.
            extras = record.o2mConceptos.filtered(lambda concepto: not concepto.m2oTipoConcepto.bEsDeduccion)
            #Saca el valor de su campo fImporte con mapped, los sumo y guardo en fTotalDeducciones.
            record.fTotalDeducciones = sum(deducciones.mapped('fImporte'))
            #Al salario bruto le sumo los extras, resto las deducciones y obtengo el salario neto.
            record.fSalarioNeto = record.fSalarioBruto + sum(extras.mapped('fImporte')) - record.fTotalDeducciones

    #Validación: El salario neto no puede ser negativo.
    @api.constrains('fSalarioNeto')
    def validacion_salario_neto(self):
        for nomina in self:
            if nomina.fSalarioNeto < 0:
                raise ValidationError('El salario neto no puede ser negativo')

    #Validación: Comprueba si ya existe una nómina igual.
    @api.constrains('m2oContrato', 'sPeriodoMes', 'iPeriodoAnio')
    def validacion_duplicados_nomina(self):
        for nomina in self:
            nomina_repe = self.search_count([
                ('id', '!=', nomina.id),                         #No sea esta misma nómina
                ('m2oContrato', '=', nomina.m2oContrato.id),     #Mismo contrato
                ('sPeriodoMes', '=', nomina.sPeriodoMes),        #Mismo mes
                ('iPeriodoAnio', '=', nomina.iPeriodoAnio),       #Mismo año
            ]) 
            if nomina_repe:
                raise ValidationError('Ya existe una nómina de este contrato para ese mes y año')

    #Validación: Se exige que la nómina tenga un concepto.
    @api.constrains('bEmitida', 'o2mConceptos')
    def validacion_emitida(self):
        for nomina in self:
                if nomina.bEmitida and not nomina.o2mConceptos:
                    raise ValidationError('Para emitir una nómina necesita un concepto')