# -*- coding: utf-8 -*-
{
    'name': 'hana project',
    'version': '1.0',
    'category': 'Project ',
    'description': "Add field project to the user also for the employee ",
    'author': "Aymen RAHMANI",
    'depends': ['base','project','hr','hana_ksa_region_city'],
    'data': [
            'views/model_view.xml',
            'views/sequence.xml',
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
