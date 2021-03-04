# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ShipmentOrder(models.Model):
    _name = 'shipment.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Shipment Order'
    _order = "date_order desc"

    def get_moves_count(self):
        moves = self.env['account.move'].search([('ref_id', '=', self.id)])
        self.bills_count = len(moves.filtered(lambda b: b.type == 'in_invoice' and not b.commission))
        self.commission_count = len(moves.filtered(lambda b: b.type == 'in_invoice' and b.commission))
        self.invoices_count = len(moves.filtered(lambda i: i.type == 'out_invoice'))

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
        required=True
    )

    to_country_id = fields.Many2one(
        string='To',
        comodel_name='res.country',
        required=True
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
    
    
    
    
    # inv_id = fields.Many2one(
    #     string='Invoive Ref',
    #     comodel_name='account.move',
    #     copy=False
    # )
    # bill_id = fields.Many2one(
    #     string='Bill Ref',
    #     comodel_name='account.move',
    #     copy=False
        
    # )
    
    narration = fields.Text(
        string='narration',
    )
    
    invoiced = fields.Boolean(
        string='invoice',
    )
    billed = fields.Boolean(
        string='bill',
    )
    
    bills_count = fields.Integer(string='Bills', compute='get_moves_count')
    commission_count = fields.Integer(string='Commission', compute='get_moves_count')
    invoices_count = fields.Integer(string='Invoices', compute='get_moves_count')
    
    
    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
    
    #     result = super(ShipmentOrder, self).create(vals)
    #     return result

    def open_commission(self):
        return {
            'name': _('Commission'),
            'domain': [('ref_id', '=', self.id),('type', '=', 'in_invoice'),('commission', '=', True)],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    def open_vendor_bills(self):
        return {
            'name': _('Vendor Bills'),
            'domain': [('ref_id', '=', self.id),('type', '=', 'in_invoice')],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def open_customer_invoices(self):
        return {
            'name': _('Customer Invoices'),
            'domain': [('ref_id', '=', self.id),('type', '=', 'out_invoice')],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    def action_confirm(self):
        if not self.line_ids:
            raise UserError(_("You should add at least on container to the order"))
        self.state = 'confirm'
        
    
    def action_close(self):
        self.state = 'done'

    def create_customer_invocie(self):
        #this method is called to open wizard,
        # of how user wants to create the customer invoice
        context = dict(self.env.context)
        context['invoice_type'] = 'out'
        return {
            'name': "Create Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.invoice',
            'view_id': self.env.ref('shipment.create_invoice_form').id,
            'target': 'new',
            'context': context
        }
        
    
    def create_vendor_bill(self):
         #this method is called to open wizard,
        # of how user wants to create the vendor invoice
        context = dict(self.env.context)
        context['invoice_type'] = 'in'
        return {
            'name': "Create Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.invoice',
            'view_id': self.env.ref('shipment.create_invoice_form').id,
            'target': 'new',
            'context': context
        }

    def create_commission(self):
        print("self id -------",self.id)
        print("context.get('active_id'---------------",self.env.context.get('active_id'))
        invoice_vals = {
        'partner_id': False,
        'ref_id':self.id,
        'state': 'draft',
        'commission':True,
        'type': 'in_invoice',
        'invoice_date': self.date_order,
        'invoice_line_ids':False,
        }
        move = self.env['account.move'].sudo().create(invoice_vals)
        print("move----------",move.ref_id , move.commission)
        return {
            'name': _('Commission'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id':move.id
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
    
    