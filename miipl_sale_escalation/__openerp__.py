# -*- coding: utf-8 -*-
{
    'name': "miipl sale escalation",

    'summary': """
        Product price updation and Price requisitions.
        """,

    'description': """
        This module allow to request for new products addition add allows to update product price updation
    """,

    'author': "Optibiz India",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','miipl_wkf'],
    # always loaded
    'data': [


        'views/sale_config.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
