from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import formatLang, format_date, get_lang


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def compute_currency_with_rate(self,mve,total,rate,currency_id ):
        amount = rate * total
        print("am,ount=========",amount)
        lang_env = mve.with_context(lang=mve.partner_id.lang).env
        # amount_convert = formatLang(lang_env, amount, currency_obj=currency_id)
        print("amount conver============",amount)
        return amount
