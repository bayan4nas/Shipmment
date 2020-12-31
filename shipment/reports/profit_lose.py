from odoo import api, models,fields,  _


class ProfitReport(models.AbstractModel):
    _name = 'report.shipment.profit_lose_report'
    _description = 'Profit & Lose Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        start = data['form']['start']
        end = data['form']['end']
        domain = [('date_order','>=',start),('date_order','<=',end)]
        if data['form']['policy_ids']:
            domain += [('id','in',data['form']['policy_ids'])]

        shipments = self.env['shipment.order'].search(domain)
       
       
        return {
            'doc_model': 'account.move',
            'docs': docids,
            'data': data['form'],
            'result':shipments,
        }
