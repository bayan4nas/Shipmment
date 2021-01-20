from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
           if self.search_count([('name','=',self.name)]) > 1:
               raise ValidationError(_("You cant have two products with the same name, please choose different name"))
            
    