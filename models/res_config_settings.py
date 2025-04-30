from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    myoperator_webhook_url = fields.Char(
        string='Webhook URL',
        readonly=True,
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url', '') + '/myoperator/webhook'
    )
    
    myoperator_webhook_secret = fields.Char(
        string='Webhook Secret',
        config_parameter='myoperator_webhook_integration.webhook_secret'
    )
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['myoperator_webhook_url'] = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url', '') + '/myoperator/webhook'
        res['myoperator_webhook_secret'] = self.env['ir.config_parameter'].sudo().get_param(
            'myoperator_webhook_integration.webhook_secret', '')
        return res
