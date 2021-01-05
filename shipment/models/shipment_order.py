# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ShipmentOrder(models.Model):
    _name = 'shipment.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Shipment Order'
    _order = "date_order desc"
    name = fields.Char(string='Policy Number', required=True,)
    customer_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        required=True,
       
        
    )

    vendor_id = fields.Many2one(
        string='Vendor',
        comodel_name='res.partner',
        required=True
       
        
    )

    
    from_country_id = fields.Many2one(
        string='From',
        comodel_name='res.country',
        ondelete='restrict',
    )

    to_country_id = fields.Many2one(
        string='To',
        comodel_name='res.country',
    )
    
    
    
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'confrim'),('done', 'Done')],string='State',default='draft'
    )
    
    date_order = fields.Date(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Date.context_today, help="Creation date of draft orders,\nConfirmation date of confirmed orders.")
    
    line_ids = fields.One2many(
        string='line',
        comodel_name='shipment.order.line',
        inverse_name='shipment_id',
    )
    
    inv_id = fields.Many2one(
        string='Invoive Ref',
        comodel_name='account.move',
    )
    bill_id = fields.Many2one(
        string='Bill Ref',
        comodel_name='account.move',
    )
    
    narration = fields.Text(
        string='narration',
    )
    
    invoiced = fields.Boolean(
        string='invoice',
    )
    billed = fields.Boolean(
        string='bill',
    )
    
    
    
    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
    
    #     result = super(ShipmentOrder, self).create(vals)
    #     return result

    def create_moves(self,invoice_type):
        """call this method with type 'in' t create bill or /
        type 'out' to create invocie"""

        invoice_vals = {
        'partner_id': self.customer_id.id if invoice_type == 'out' else self.vendor_id.id,
        'state': 'draft',
        'policy_id':self.id,
        'type': 'out_invoice' if invoice_type == 'out' else 'in_invoice',
        'invoice_date': self.date_order,
        'invoice_line_ids': [(0, 0, {
            'product_id':line.product_id.id,
            'name': line.name,
            'quantity': line.qty,
            'price_unit': 0,
            }) for line in self.line_ids],
        }
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        if invoice_type == 'out':
            self.write({'inv_id':invoice.id,'invoiced':True})
            
        else:
            self.write({'bill_id':invoice.id,'billed':True})
        
        return invoice
        
    def action_confirm(self):
        self.state = 'confirm'
    
    def create_customer_invocie(self):
        if not self.line_ids:
            raise ValidationError(_("""You cannot create invoice without lines"""))
        inv_id = self.create_moves(invoice_type='out')
        self.state = 'done'
        return {
            'name': _('Accont Move'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id':inv_id.id
            # 'domain': [('id', 'in', ids)],
        }
    
    def create_vendor_bill(self):
        if not self.line_ids:
            raise ValidationError(_("""You cannot create bill without lines"""))
        bill_id = self.create_moves(invoice_type='in')
        return {
            'name': _('Accont Move'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id':bill_id.id
            # 'domain': [('id', 'in', ids)],
        }

class ShipmentOrderLine(models.Model):
    _name = 'shipment.order.line'
    _description = 'Shipment Order Line'
    
    name = fields.Char(
        string='name',
        related='product_id.name',
        readonly=True,
        store=True
        
    )
    
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        required=True,
        domain="[('type', '=', 'service')]",
        
        
    )
    
    qty = fields.Char(string="quantity",
    required=True
    )

    shipment_id = fields.Many2one(
        string='Order Ref',
        comodel_name='shipment.order',
    )
    
    cost = fields.Float(
        string='Cost',
    )
    
    