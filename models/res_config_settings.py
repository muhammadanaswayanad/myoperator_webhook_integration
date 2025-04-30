from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    myoperator_webhook_url = fields.Char(
        string='Webhook URL',
        readonly=True,
        compute='_compute_webhook_url'
    )
    
    myoperator_webhook_secret = fields.Char(
        string='Webhook Secret',
        config_parameter='myoperator_webhook_integration.webhook_secret'
    )

    @api.depends('company_id')
    def _compute_webhook_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        for record in self:
            record.myoperator_webhook_url = f"{base_url}/myoperator/webhook"
