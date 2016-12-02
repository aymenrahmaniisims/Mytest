# -*- coding: utf-8 -*-
{
    'name': 'hana catering',
    'version': '1.0',
    'category': 'Catering',
    'description': "Create the week plans, Diet orders ...",
    'author': "Aymen RAHMANI",
    'depends': ['base','hana_project','hr','project','purchase'],
    'data': [
            'views/menu_view.xml',
            'views/sequence.xml',
            'views/model_view.xml',
            'views/diet_order_view.xml',
            'views/week_plan_view.xml',
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
