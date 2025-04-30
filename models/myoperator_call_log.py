from odoo import models, fields, api

class MyOperatorCallLog(models.Model):
    _name = "myoperator.call.log"
    _description = "MyOperator Call Log"
    _rec_name = "name"
    _order = "call_time desc"

    name = fields.Char(string="Call ID", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    call_status = fields.Selection([
        ('missed', 'Missed'),
        ('answered', 'Answered'),
        ('voicemail', 'Voicemail')
    ], string="Call Status", required=True)
    call_duration = fields.Integer(string="Call Duration (sec)", default=0)
    call_time = fields.Datetime(string="Call Time", default=fields.Datetime.now)
    call_notes = fields.Text(string="Notes")
    
    # Links to CRM and contacts
    partner_id = fields.Many2one('res.partner', string="Contact")
    lead_id = fields.Many2one('crm.lead', string="Lead/Opportunity")
