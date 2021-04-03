from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    line = fields.Boolean(
        string='Line?',
    )

    customer = fields.Boolean(
        string='Customer?',
    )
    