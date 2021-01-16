from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'res.bank'

    
    iban_no = fields.Char(
        string='Iban No',
    )
    
  
    branch = fields.Char(
      string='Branch',
    )
  
    