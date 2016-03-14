# -*- coding: utf-8 -*-
{
    'name': "miipl Purchase Warehouse Access",

    'summary': """
        This Module give the access to purchase and warehouse to sale price history and product price history from optibiz""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optibiz India",
    'website': "http://optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','miipl_product_requisition','stock','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
