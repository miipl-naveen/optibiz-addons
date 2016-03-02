# -*- coding: utf-8 -*-
{
    'name': "miipl_product_history",

    'summary': """
        This module will allow to check the product price history
        """,

    'description': """
        This module will allow to check the product price history
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','miipl_msp'],

    # always loaded
    'data': ['views/product_history.xml',
             #'security/ir.model.access.csv',
             #'security/miipl_product_validation_security.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}