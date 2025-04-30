import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class MyOperatorWebhookController(http.Controller):
    
    @http.route('/myoperator/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def myoperator_webhook_handler(self):
        """Handle incoming webhook data from MyOperator"""
        try:
            # Get the webhook secret for verification if needed
            webhook_secret = request.env['ir.config_parameter'].sudo().get_param(
                'myoperator_webhook_integration.webhook_secret'
            )
            
            # Get the JSON data
            data = request.jsonrequest
            _logger.info("Received MyOperator webhook data: %s", json.dumps(data))
            
            # Validate required fields
            required_fields = ['caller_number']
            if not all(field in data for field in required_fields):
                _logger.error("Missing required fields in webhook data")
                return {'status': 'error', 'message': 'Missing required fields'}
            
            # Process webhook data
            call_log = request.env['myoperator.call.log'].sudo().create_from_webhook(data)
            
            return {'status': 'success', 'message': 'Webhook processed successfully', 'call_log_id': call_log.id}
            
        except Exception as e:
            _logger.exception("Error processing MyOperator webhook: %s", str(e))
            return {'status': 'error', 'message': str(e)}
