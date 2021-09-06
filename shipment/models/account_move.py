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
        compute="get_rate_currency",
        store=True,
    )

    company_currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        default=lambda self: self.env.user.company_id.currency_id
        
    )

    inv_seq = fields.Char(string='Invoice ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    

    
    ref_id = fields.Many2one(
        string='Reference',
        comodel_name='shipment.order',
    )

    credit_not_id = fields.Many2one(
        string='Credit Note',
        comodel_name='account.move',
    )

    
    commission = fields.Boolean(
        string='Commission',
        readonly=True 
        
    )
    
    remark = fields.Char('Remark')

    is_ship = fields.Boolean('Shipment Bill/Invoice')  


    @api.onchange('partner_id')
    def get_partner_bank_account(self):
        if self.partner_id :
            bank_ids = self.partner_id.bank_ids
            self.invoice_partner_bank_id = bank_ids and bank_ids[0].id or False

    def print_payment(self):
        paymenet_id = self.env.get('account.payment').search([('invoice_ids', 'in',[self.id])])
        return self.env.ref('account.action_report_payment_receipt').report_action(paymenet_id)


    @api.model
    def create(self, vals):
        # overriding the create method to add the sequence
        if vals.get('inv_seq', _('New')) == _('New'):
            vals['inv_seq'] = self.env['ir.sequence'].next_by_code('account.move.seq') or _('New')
        result = super(AccountMove, self).create(vals)
        result.get_partner_bank_account()
        return result
    
    @api.depends('rate_currency_id','currency_id')    
    def get_rate_currency(self):
        if self.rate_currency_id and self.currency_id :
            rate = self.currency_id._convert(1, self.rate_currency_id, self.env['res.company'].browse(1), self.invoice_date or fields.Date.today())
            self.charge_amount = rate 
        
    def compute_currency_with_rate(self,mve,total,rate,currency_id ):
        #call the method from report with amount , currency and date to get amount in company currency and vis versa
        amount = rate * total
        lang_env = mve.with_context(lang=mve.partner_id.lang).env
        
        return amount
       

    def compute_currency_without_rate(self,total,date_order,currency_id ):
        
       #call the method from report with amount , currency and date to get amount in company currency and vis versa
        company_currency = self.env.user.company_id.currency_id
        if currency_id != company_currency.id:
            amount_convert = self.env['res.currency'].browse(currency_id)._convert(total, company_currency, self.env.user.company_id, date_order or fields.Date.today())
        
            return round(amount_convert,3)
        return total
                
       
    def action_post(self):
        #override post method to make sure :
        # customer invoice is greater than vendor bill
        for rec in self:
            #get related vendor bill before posting
            if rec.ref_id and not rec.commission and rec.type == 'out_invoice':
                bills = self.search([('ref_id','=',rec.ref_id.id),('type','=','in_invoice'),('commission','=',False)])
                total_bills_amount = sum(bills.mapped('amount_total'))
                if self.amount_total <= total_bills_amount:
                    raise UserError(_("Customer invoice amount not Acceptaple !!"))
            elif rec.ref_id and rec.commission:
                bills = self.search([('ref_id','=',rec.ref_id.id),('type','=','in_invoice'),('commission','!=',True)])
                invoices = self.search([('ref_id','=',rec.ref_id.id),('type','=','out_invoice')])
                total_amount = sum(invoices.mapped('amount_total')) -  sum(bills.mapped('amount_total'))
               
                if rec.amount_total > total_amount:
                    raise UserError(_("Commission amount not Acceptaple !!"))
        return super(AccountMove, self).action_post()
        
        