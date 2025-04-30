{
    'name': 'MyOperator Webhook Integration',
    'version': '1.0',
    'summary': 'Integrate MyOperator call logs via webhooks',
    'description': """
        This module integrates MyOperator call data into Odoo via webhooks.
        Track call logs and integrate with CRM leads and contacts.
    """,
    'category': 'CRM',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/myoperator_call_log_views.xml',
        'views/res_config_settings_views.xml',
        'views/myoperator_menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
