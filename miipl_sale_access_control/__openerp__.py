# -*- coding: utf-8 -*-
{
    'name': "miipl_sale_access_control",

    'summary': """
        This module will allow to create new access role 'Sales Team Lead'
        """,

    'description': """
        This module will allow to create new access role 'Sales Team Lead'
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock','crm'],

    # always loaded
    'data': [
         #'security/ir.model.access.csv',
        'security/sale_security.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}