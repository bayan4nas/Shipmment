# -*- coding: utf-8 -*-

from odoo import models, fields


class CreateAppointment(models.TransientModel):
    _name = 'profit.lose.report'
    _description = 'Create Profit & Lose Wizard'

    
    start = fields.Date(
        string='Start',
        default=fields.Date.context_today,
        required=True
    )

    end = fields.Date(
        string='End',
        default=fields.Date.context_today,
        required=True
        
    )
    
    policy_ids = fields.Many2many(
        string='Policy',
        comodel_name='shipment.order',
    )
    
    
    currency = fields.Selection(
        string='Currency',
        selection=[('company', 'Company Currency'), ('usd', 'USD')],default="company"
    )
    
    
    commission = fields.Boolean(
        string='Show Commission?',
    )
    

    

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'profit.lose.report',
            'form': data
        }
        return self.env.ref('shipment.action_profit_lose_report').report_action(self.id,datas)
    def print_excel_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'profit.lose.report',
            'form': data
        }
        return self.env.ref('shipment.action_shipment_xls').report_action(self.id,datas)