from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Bank(models.Model):
    _inherit = 'res.bank'

    branch = fields.Char(
      string='Branch',
    )
  

class PartnerBank(models.Model):
    _inherit = 'res.partner.bank'
   
    iban_no = fields.Char(
        string='Iban No',
    )
    branch = fields.Char(related='bank_id.branch', readonly=False)
    