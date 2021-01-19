from odoo import models, fields, api, _

class PaymentChargeType(models.Model):
    _name = 'payment.charge.type'
    
    name = fields.Char(
        string='Name',
    )
    