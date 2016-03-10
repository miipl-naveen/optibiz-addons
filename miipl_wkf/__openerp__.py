# -*- coding: utf-8 -*-
{
    'name': "miipl_wkf",

    'summary': """
        Implementation for the approval work flow for MIIPL sales order.
        """,

    'description': """
        This module adds workflows and transitions for approval of sales order and quotation within MIIPL
    """,

    'author': "Optibiz India",
    'website': "http://www.optibiz.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','crm','miipl_msp','miipl_sale_access_control','miipl_product_price_validation'],

    # always loaded
    'data': [
        #'security/sale_security.xml',
         'security/ir.model.access.csv',
        'workflows/flows.xml',
        'views/sale_order_view.xml',
        'views/miipl_scheduler.xml',
        'email_template_project_auto.xml',
        'sale_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
