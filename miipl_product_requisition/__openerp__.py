# -*- coding: utf-8 -*-
{
    'name': "miipl Product requisitions & Price updation",

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
    'depends': ['base', 'sale','miipl_sale_access_control','miipl_product_manager','miipl_wkf','miipl_product_history','stock_account','purchase'],

    # always loaded
    'data': [


        'views/miipl_sequence.xml',
        'wizard/miipl_price_update.xml',
        'views/miipl_product_requisition.xml',
        'security/product_requisition_security.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
