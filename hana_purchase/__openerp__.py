# -*- coding: utf-8 -*-
{
    'name': 'hana purchase',
    'version': '1.0',
    'category': 'Catering',
    'description': "Create the PeriodicallyPurchaseOrder from sites ...",
    'author': "Aymen RAHMANI",
    'depends': ['base','hana_project','hana_catering','hr','purchase'],
    'data': [
            'views/menu_view.xml',
            'views/sequence.xml',
            'views/model_view.xml',
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
