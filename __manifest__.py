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

        'views/requisito_views.xml',
        'views/puesto_trabajo_views.xml',
        'views/titulo_academico_views.xml',
        'views/titulo_idioma_views.xml',
        'views/aptitud_views.xml',
        'views/lenguaje_programacion_views.xml',
        'views/material_views.xml',
        'views/menu.xml'


    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': True,
}

