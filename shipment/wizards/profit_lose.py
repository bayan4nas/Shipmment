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
    
    policy_id = fields.Many2one(
        string='Policy',
        comodel_name='shipment.order',
    )
    

    

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'profit.lose.report',
            'form': data
        }
        print("data-=========",datas)
        return self.env.ref('shipment.action_profit_lose_report').report_action(self.id,datas)
