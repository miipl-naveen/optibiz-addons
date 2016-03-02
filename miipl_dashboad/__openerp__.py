# -*- coding: utf-8 -*-
{
    'name': "miipl Dashboard",

    'summary': """
        Dashboard
        """,

    'description': """
    Dashboard
    """,

    'author': "Optibiz India",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','miipl_sale_access_control','miipl_product_manager','miipl_wkf','miipl_product_requisition'],

    # always loaded
    'data': [


        'views/dashboard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
