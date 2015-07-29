# -*- coding: utf-8 -*-
{
    'name': "purchase_terms",

    'summary': """
        Terms and conditions for purchase module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optibiz",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sale'],

    # always loaded
    'data': [
        'view_form.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
}