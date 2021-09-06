# -*- coding: utf-8 -*-

from odoo import models, fields , _


class CreateAppointment(models.TransientModel):
    _name = 'create.invoice'
    _description = 'Create Invoice Wizard'

    invocie_type = fields.Selection([('line', 'Line'),('customer','Customer Invoice'),('commission','Comission ')],string="Invoice Type")
    
    def create_empty_moves(self , invoice_type , order_id):
        #TODO THIS METHOD AND BELOW METHOD CAN BE MERGED IN ON METHOD,THEY DO THE SAME EXPECT THIS WITHOUT MOVE LINES
        """call this method with type 'in' t create bill or /
        type 'out' to create invocie"""
        order_id = self.env.get('shipment.order').browse(order_id)
        invoice_vals = {
        'partner_id': order_id.customer_id.id if invoice_type == 'out' else order_id.vendor_id.id,
        'state': 'draft',
        'policy_id':order_id.id,
        'ref_id':order_id.id,
        'type': 'out_invoice' if invoice_type == 'out' else 'in_invoice',
        'invoice_date': order_id.date_order,
        }
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        # if invoice_type == 'out':
        #     order_id.write({'inv_id':invoice.id,})
            
        # else:
        #     order_id.write({'bill_id':invoice.id,})
        
        return invoice


    def create_moves(self , invoice_type , order_id):
        """call this method with type 'in' t create bill or /
        type 'out' to create invocie"""

        order_id = self.env.get('shipment.order').browse(order_id)
        price_unit_key = 'cost'
        if invoice_type == 'out' : price_unit_key = 'price'
        elif self.invocie_type == 'commission' : price_unit_key = 'commission'
        invoice_vals = {
        'partner_id': order_id.customer_id.id if invoice_type == 'out' else order_id.vendor_id.id,
        'state': 'draft',
        'policy_id':order_id.id,
        'ref_id':order_id.id,
        'type': 'out_invoice' if invoice_type == 'out' else 'in_invoice',
        'invoice_date': order_id.date_order,
        'commission': self.invocie_type == 'commission',
        'invoice_line_ids': [(0, 0, {
            'product_id':line.product_id.id,
            'name': line.name,
            'quantity': line.qty,
            'price_unit': line[price_unit_key],
            }) for line in order_id.line_ids],
        }
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        # if invoice_type == 'out':
        #     order_id.write({'inv_id':invoice.id,'invoiced':True})
            
        # else:
        #     order_id.write({'bill_id':invoice.id,'billed':True})
        
        return invoice

        
    def empty_invoice(self):
        ctx = self._context
        move_id = self.create_empty_moves(ctx.get('invoice_type') , order_id = ctx.get('active_id') )
        return {
            'name': _('Accont Move'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id':move_id.id
            # 'domain': [('id', 'in', ids)],
        }

    def invoice_line(self):
        ctx = self._context
        move_id = self.create_moves(ctx.get('invoice_type') , order_id = ctx.get('active_id') )
        return {
            'name': _('Accont Move'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id':move_id.id,
            # 'domain': [('id', 'in', ids)],
            'view_id': self.env.ref('shipment.inherit_account_view_move_form').id,
        }

    
        