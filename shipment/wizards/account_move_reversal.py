from odoo import models, fields, api, _
from odoo.tools.translate import _



class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'
    def reverse_moves(self):
        res =  super(AccountMoveReversal, self).reverse_moves()
        if self.move_id.type == 'out_invoice':
            self.move_id.credit_not_id = res['res_id']
        return res