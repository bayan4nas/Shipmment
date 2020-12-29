# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ShipmentOrder(models.Model):
    _name = 'shipment.order'
    _description = 'Shipment Order'

    name = fields.Char(string='Shipment Number', required=True, readonly=True, default=lambda self: _('New'), copy=False)
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=True
        
    )
    
    
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('confirm', 'confrim'),('invoice', 'Invoiced'),('bill', 'Billed')],default='draft'
    )
    
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft orders,\nConfirmation date of confirmed orders.")
    
    line_ids = fields.One2many(
        string='line',
        comodel_name='shipment.order.line',
        inverse_name='shipment_id',
    )
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
    
        result = super(ShipmentOrder, self).create(vals)
        return result

    def create_moves(self,invoice_type):
        invoice_vals = {
        'partner_id': self.partner_id.id,
        'state': 'draft',
        'type': 'out_invoice' if invoice_type == 'out' else 'in_invoice',
        'invoice_date': self.date_order,
        'invoice_line_ids': [(0, 0, {
            'product_id':line.product_id.id,
            'name': line.name,
            'quantity': line.qty,
            'price_unit': line.cost,
            }) for line in self.line_ids],
        }
        invoice = self.env['account.move'].sudo().create(invoice_vals)

    def action_confirm(self):
        self.state = 'confirm'
    
    def create_customer_invocie(self):
        if not self.line_ids:
            raise ValidationError(_("""You cannot create invoice without lines"""))
        self.create_moves(invoice_type='out')
        self.state = 'invoice'
    
    def create_vendor_bill(self):
        if not self.line_ids:
            raise ValidationError(_("""You cannot create bill without lines"""))
        self.create_moves(invoice_type='in')
        self.state = 'bill'

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
        required=True
        
    )
    
    qty = fields.Char(string="quantity",
    required=True
    )

    shipment_id = fields.Many2one(
        string='shipment.order.id',
        comodel_name='shipment.order',
    )
    
    cost = fields.Float(
        string='Cost',
    )
    
    