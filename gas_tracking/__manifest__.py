# -*- coding: utf-8 -*-
{
    'name': "LPG Gas Tracking",

    'summary': """
        A module to manage and track LPG gas cylinders, including refills, customer tracking, and scheduling.
    """,

    'description': """
        The LPG Gas Tracking module is designed to streamline the management and tracking of LPG gas cylinders. 
        This module allows gas agencies to:
        
        - Maintain detailed records of each gas cylinder, including serial number, refill status, and last refill date.
        - Track customers (stores) and associate cylinders with them.
        - Schedule and manage gas refills for groups of cylinders.
        - Identify cylinders that have not been refilled within a specified timeframe.
        - Record transactions, noting the status of the cylinder (full or empty) and the associated customer.
        - Ensure proper handling and verification of cylinders when returned empty.

        Key features:
        - Detailed tracking of gas cylinders.
        - Customer and staff management.
        - Refill scheduling and notifications.
        - Comprehensive transaction logging.
    """,

    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'hr','crm','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/gas_product_views.xml',
        'views/gas_staff_views.xml',
        'views/gas_store_views.xml',
        'views/gas_transaction_views.xml',
        'views/gas_overview_views.xml',
        'views/purchase_views.xml',
    ],
}
