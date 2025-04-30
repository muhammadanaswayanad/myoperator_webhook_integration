from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    myoperator_webhook_secret = fields.Char(
        string='MyOperator Webhook Secret',
        config_parameter='myoperator_webhook_integration.webhook_secret'
    )
    
    myoperator_webhook_url = fields.Char(
        string='Webhook URL',
        compute='_compute_webhook_url',
        readonly=True
    )
    
    @api.depends('company_id')
    def _compute_webhook_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            record.myoperator_webhook_url = f"{base_url}/myoperator/webhook"
