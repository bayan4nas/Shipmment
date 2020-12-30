from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    policy_id = fields.Many2one(
        string='Policy',
        comodel_name='shipment.order',
    )
    