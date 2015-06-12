# -*- coding: utf-8 -*-
{
    'name': "miipl_credit_limit",

    'summary': """
        This module will not allow the confirmation of sale order for a customer if the
        credit limit is reached
        """,

    'description': """
        This module will not allow the confirmation of sale order for a customer if the
        credit limit is reached
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}