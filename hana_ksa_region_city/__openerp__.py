# -*- coding: utf-8 -*-
{
    'name': 'KSA region City',
    'version': '1.0',
    'category': 'Sale ',
    'description': "MAke the KSA region and city with city code based on region code ",
    'author': "Aymen RAHMANI",
    'depends': ['base','project'],
    'data': [
            'security/ir.model.access.csv',
            'views/ksa_region_city_view.xml',
            'data/template.xml',
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
