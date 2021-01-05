from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    #add policy ref to account move ,
    #when create bill or invoice ,
    # it will automatically link to its policy by this field
    policy_id = fields.Many2one(
        string='Policy Ref',
        comodel_name='shipment.order',
    )
    def compute_currency(self,total,currency,date_order):
       
        company_currency = self.env.user.company_id.currency_id
        currency_id = self.env['res.currency'].search([('id', '=', currency.id)])
        if company_currency != currency_id:
            amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency )
            return amount_convert
        return total