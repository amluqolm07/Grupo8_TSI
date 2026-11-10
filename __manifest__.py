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
        'views/menu.xml',
        #Demos por aqui
    ],
    
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    
    'application': True,
}

