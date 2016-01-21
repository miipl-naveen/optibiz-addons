# -*- coding: utf-8 -*-
{
    'name': "miipl_product_price_validation",

    'summary': """
        This module will allow to check the last modification product price
        """,

    'description': """
        This module will allow to check the last modification product price
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock'],

    # always loaded
    'data': ['models/product_price_validation.xml',
             'models/product_config.xml'
         #'security/ir.model.access.csv',
        #'security/miipl_product_validation_security.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}