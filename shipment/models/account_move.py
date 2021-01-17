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
    
    charge = fields.Char(
        string='Charge',
    )
    charge_amount = fields.Float(
        string='Charge Amount',
    )

    company_currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        default=lambda self: self.env.user.company_id.currency_id
        
    )
    
    def compute_currency(self,total,date_order,currency_id ,is_company):
       #call the method from report with amount , currency and date to get amount in company currency and vis versa
        company_currency = self.env.user.company_id.currency_id
        currency_id = self.env['res.currency'].search([('id', '=', currency_id)])
        
        if not is_company:
            amount_convert = currency_id._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
            # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency )
            #     return round(amount_convert,3)
            # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency)
            return round(amount_convert,3)
        return total
       
