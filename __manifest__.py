# -*- coding: utf-8 -*-
{
    'name': "RRHH_UPO",

    'summary': "Gestion del modulo de Recursos Humanos para la UPO",

    'description': """En este modulo se gestionan solicitudes en base a ofertas de empleo asi como contratos, 
    nominas y rendimiento general de empleados de la UPO.""",

    'author': "Grupo 8",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        #Vistas
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/cita_views.xml',
        'views/entrevista_views.xml',
        'views/historial_laboral_views.xml',
        'views/parte_horario_views.xml',
        'views/sala_views.xml',
        'views/sesion_views.xml',
        'views/tipo_cita_views.xml',
        'views/tipo_entrevista_views.xml',
        'views/tipo_sala_views.xml',
        'views/tipo_sesion_views.xml',
        #Demos por aqui, importa el orden
        'demo/rrhh_upo.cita.csv',
        'demo/rrhh_upo.entrevista.csv',
        'demo/rrhh_upo.sala.csv',
        'demo/rrhh_upo.sesion.csv',
        'demo/rrhh_upo.tipo_cita.csv',
        'demo/rrhh_upo.tipo_entrevista.csv',
        'demo/rrhh_upo.tipo_sala.csv',
        'demo/rrhh_upo.tipo_sesion.csv',
        #Empleado
        'demo/rrhh_upo.historial_laboral.csv',
        'demo/rrhh_upo.parte_horario.csv',
    ],
    
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    
    'application': True,
}

