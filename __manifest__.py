# -*- coding: utf-8 -*-
{
    'name': "rrhh_upo",

    'summary': "Gestion del modulo de Recursos Humanos para la UPO",

    'description': """En este modulo se gestionan solicitudes en base a ofertas de empleo asi como contratos, 
    nominas y rendimiento general de empleados de la UPO.
    """,

    'author': "Grupo 8",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_recruitment', 'hr_skills'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        #Vistas
        'views/views.xml',
        'views/cita_views.xml',
        'views/entrevista_views.xml',
        'views/historial_laboral_views.xml',
        'views/sala_views.xml',
        'views/sesion_views.xml',
        'views/menu.xml',
        #Demos por aqui, importa el orden
        'demo/rrhh_upo.cita.csv',
        'demo/rrhh_upo.entrevista.csv',
        'demo/rrhh_upo.sala.csv',
        'demo/rrhh_upo.sesion.csv',
        'demo/rrhh_upo.historial_laboral.csv',

        'views/requisito_views.xml',
        'views/puesto_trabajo_views.xml',
        'views/titulo_academico_views.xml',
        'views/titulo_idioma_views.xml',
        'views/aptitud_views.xml',
        'views/lenguaje_programacion_views.xml',
        'views/material_views.xml',
        'views/menu.xml'


        'views/asignatura_views.xml',
        'views/departamento_views.xml',
        'views/equipo_investigacion_views.xml',
        'views/expediente_views.xml',
        'views/financiacion_views.xml',
        'views/grado_views.xml',
        'views/investigacion_views.xml',
        'views/matricula_views.xml',
        'views/solicitud_views.xml',
        'views/tipo_investigacion_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/tipo_contrato_views.xml',
        'views/contrato_views.xml',
        'views/nomina_views.xml',
        'views/concepto_views.xml',
        'views/tipo_concepto_views.xml'
        'views/menu.xml',
        #Demos por aqui
        'demo/rrhh_upo.tipo_concepto.csv',
        'demo/rrhh_upo.tipo_contrato.csv',
        'demo/rrhh_upo.solicitud.csv',
        'demo/rrhh_upo.contrato.csv',
        'demo/rrhh_upo.nomina.csv',
        'demo/rrhh_upo.concepto.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': True,
}

