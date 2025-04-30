from odoo import api, fields, models, _
from datetime import datetime

class MyOperatorCallLog(models.Model):
    _name = 'myoperator.call.log'
    _description = 'MyOperator Call Log'
    _order = 'call_start_time desc'
    _rec_name = 'caller_number'

    caller_number = fields.Char('Caller Number', required=True, index=True)
    receiver_number = fields.Char('Receiver Number')
    call_start_time = fields.Datetime('Call Start Time')
    call_end_time = fields.Datetime('Call End Time')
    call_duration = fields.Integer('Call Duration (seconds)')
    call_status = fields.Char('Call Status')
    call_recording_url = fields.Char('Call Recording URL')
    
    lead_id = fields.Many2one('crm.lead', string='Related Lead')
    partner_id = fields.Many2one('res.partner', string='Related Contact')

    def name_get(self):
        result = []
        for record in self:
            date_str = ''
            if record.call_start_time:
                date_str = fields.Datetime.to_string(record.call_start_time)[:16]
            name = f"{record.caller_number} ({date_str})"
            result.append((record.id, name))
        return result

    @api.model
    def create_from_webhook(self, data):
        """Create a call log and update or create lead from webhook data"""
        # Create the call log
        vals = {
            'caller_number': data.get('caller_number'),
            'receiver_number': data.get('receiver_number'),
            'call_start_time': data.get('call_start_time'),
            'call_end_time': data.get('call_end_time'),
            'call_duration': data.get('call_duration'),
            'call_status': data.get('call_status'),
            'call_recording_url': data.get('call_recording_url'),
        }
        
        # Check if there's a matching partner or lead
        caller_number = data.get('caller_number')
        partner = self.env['res.partner'].search([('phone', '=', caller_number)], limit=1)
        lead = self.env['crm.lead'].search([('phone', '=', caller_number)], limit=1)
        
        if partner:
            vals['partner_id'] = partner.id
        
        if lead:
            vals['lead_id'] = lead.id
            # Update lead with call information
            lead.write({
                'description': self._update_description(lead.description, data)
            })
        else:
            # Create new lead
            lead_vals = {
                'name': f"Inbound Call from {caller_number}",
                'phone': caller_number,
                'description': self._create_description(data),
                'type': 'lead',
            }
            new_lead = self.env['crm.lead'].create(lead_vals)
            vals['lead_id'] = new_lead.id
        
        return self.create(vals)
    
    def _create_description(self, data):
        """Create a description for a new lead"""
        description = f"""
Inbound call received from: {data.get('caller_number')}
Call Duration: {data.get('call_duration')} seconds
Call Status: {data.get('call_status', 'Unknown')}
"""
        if data.get('call_recording_url'):
            description += f"\nCall Recording: {data.get('call_recording_url')}"
        
        return description
    
    def _update_description(self, existing_description, data):
        """Update the description of an existing lead"""
        call_info = f"""
\n--- New Call Log ({fields.Datetime.now()}) ---
Inbound call received from: {data.get('caller_number')}
Call Duration: {data.get('call_duration')} seconds
Call Status: {data.get('call_status', 'Unknown')}
"""
        if data.get('call_recording_url'):
            call_info += f"\nCall Recording: {data.get('call_recording_url')}"
        
        return (existing_description or '') + call_info
