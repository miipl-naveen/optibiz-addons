# -*- coding: utf-8 -*-
{
    'name': "optibiz",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optibiz India",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'optibiz_landmark.xml',
        'optibiz_report.xml',
        'optibiz_sequence.xml',
        'views/report_header.xml',
        'views/report_saleorder.xml',
        'views/report_stockpicking.xml',
        'views/report_invoice.xml',
        'views/report_purchaseorder.xml',
        'views/report_purchasequotation.xml',
        'views/website_variants.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'css': ['static/src/css/optibiz.css'],
}
