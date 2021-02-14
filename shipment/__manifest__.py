# -*- coding: utf-8 -*-
{
    'name': "Shipment",

    'summary': """
        Shipment orders""",

    'description': """
       This module helps to manage your shimpent invoices and bills
    """,

    'author': "Omix",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizards/profit_lose.xml',
        'wizards/create_invoice.xml',
        'reports/report_shipment_profit_lose.xml',
        'reports/report.xml',
        'reports/external_layout.xml',
        'reports/report_invoice_shipment.xml',
        'reports/report_payment_receipt_template.xml',
        'views/shipment_order.xml',
        'views/account_move.xml',
        'views/payment_charge_type.xml',
        'views/menus.xml',
        'views/res_bank.xml',
       
        # 'views/template.xml',
        
        
    ],
    # only loaded in demonstration mode
   
}
