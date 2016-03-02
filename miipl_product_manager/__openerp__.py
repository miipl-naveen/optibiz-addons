# -*- coding: utf-8 -*-
{
    'name': "miipl_product_manager",

    'summary': """
        This module will allow to create new access role 'Product Manager'
        """,

    'description': """
        This module will allow to create new access role 'Product Manager'
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','crm','miipl_product_price_validation'],

    # always loaded
    'data': [
         'product_list.xml',
         'security/product_security.xml',
         'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}