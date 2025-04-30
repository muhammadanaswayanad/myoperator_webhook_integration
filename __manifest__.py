{
    'name': 'MyOperator Webhook Integration',
    'version': '17.0.1.0.0',
    'category': 'CRM',
    'summary': 'Integrate MyOperator webhooks with Odoo CRM',
    'description': """
        This module integrates MyOperator's webhook system with Odoo:
        - Receive After-Call webhook data from MyOperator
        - Create or update leads based on call information
        - Track call logs with detailed information
    """,
    'author': 'Odoo Developer',
    'website': '',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/myoperator_call_log_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
