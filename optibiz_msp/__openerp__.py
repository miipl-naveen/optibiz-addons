# -*- coding: utf-8 -*-
{
    'name': "optibiz_msp",

    'summary': """
        This module provides the Minimum selling price module from optibiz""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optibiz India",
    'website': "http://optibiz.in",

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
        'optibiz_product_msp.xml',
        'sale_order_view.xml',
        'security/security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}