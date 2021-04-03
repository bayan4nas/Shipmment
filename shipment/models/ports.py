from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ShipmentPort(models.Model):
    _name = 'shipment.port'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Shipment Port'

    name = fields.Char(string='Name', required=True,)
    code = fields.Char(string='Code',)
    country_id = fields.Many2one(
        string='Country',
        comodel_name='res.country',
    )

