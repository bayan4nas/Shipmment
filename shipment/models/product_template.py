from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #rewirte field to change default value
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
           if self.search_count([('name','=',self.name)]) > 1:
               raise ValidationError(_("You cant have two products with the same name, please choose different name"))
            
    