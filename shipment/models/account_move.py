from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import formatLang, format_date, get_lang


class AccountMove(models.Model):
    _inherit = 'account.move'
    #add policy ref to account move ,
    #when create bill or invoice ,
    # it will automatically link to its policy by this field
    policy_id = fields.Many2one(
        string='Policy Ref',
        comodel_name='shipment.order',
    )
    
    rate_currency_id = fields.Many2one(
        string='Currency For Layout',
        comodel_name='res.currency', 
        default=lambda self: self.env.user.company_id.currency_id
    )

    
    charge_id = fields.Many2one(
        string='Charge',
        comodel_name='payment.charge.type', 
    )

    charge_amount = fields.Float(
        string='Charge Rate',
    )

    company_currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        default=lambda self: self.env.user.company_id.currency_id
        
    )
    
   
    
    def compute_currency_with_rate(self,mve,total,rate,currency_id ):
        amount = rate * total
        print("am,ount=========",amount)
        lang_env = mve.with_context(lang=mve.partner_id.lang).env
        # amount_convert = formatLang(lang_env, amount, currency_obj=currency_id)
        print("amount conver============",amount)
        return amount
       #call the method from report with amount , currency and date to get amount in company currency and vis versa
        # company_currency = self.env.user.company_id.currency_id
        # currency_id = self.env['res.currency'].search([('id', '=', currency_id)])
        # # if company_currency.id == currency_id.id:
        # print(":currency=======",currency_id.name)
        # print(":company_currency=======",company_currency.name)
        # amount_convert = currency_id._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
        
        # lang_env = mve.with_context(lang=mve.partner_id.lang).env
        # amount_convert = formatLang(lang_env, amount_convert, currency_obj=currency_id)
        # return amount_convert
                # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency )
                #     return round(amount_convert,3)
                # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency)
        # amount_convert = currency_id._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
        # return total

    def compute_currency_without_rate(self,total,date_order,currency_id ):
        
       #call the method from report with amount , currency and date to get amount in company currency and vis versa
        company_currency = self.env.user.company_id.currency_id
        # currency_id = self.env['res.currency'].search([('id', '=', currency_id)])
        # # if company_currency.id == currency_id.id:
        # print(":currency=======",currency_id.name)
        # print(":company_currency=======",company_currency.name)
        if currency_id != company_currency:
            amount_convert = currency_id._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
        # lang_env = mve.with_context(lang=mve.partner_id.lang).env
        # amount_convert = formatLang(lang_env, amount_convert, currency_obj=currency_id)
            return round(amount_convert,3)
        return total
                # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency )
                #     return round(amount_convert,3)
                # amount_convert = currency_id.with_context(date=date_order).compute(total,company_currency)
        # amount_convert = currency_id._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
        # return total
       
