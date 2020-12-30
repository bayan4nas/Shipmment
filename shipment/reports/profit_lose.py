from odoo import api, models, _


class ProfitReport(models.AbstractModel):
    _name = 'report.shipment.profit_lose_report'
    _description = 'Profit & Lose Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("finalllllllllllllll====", data['form']['policy_id'])
        if data['form']['policy_id']:
            policies_invoice = self.env['account.move'].search([('policy_id', '=', data['form']['policy_id'][0]),('invoice_date','>=',data['form']['start']),('invoice_date','<=',data['form']['end'])])
            policies_bill = self.env['account.move'].search([('policy_id', '=', data['form']['policy_id'][0]),('invoice_date','>=',data['form']['start']),('invoice_date','<=',data['form']['end']),('type','=','out_invoice')])
        else:
            policies_invoice = self.env['account.move'].search([('invoice_date','>=',data['form']['start']),('invoice_date','<=',data['form']['end'])])
            policies_bill = self.env['account.move'].search([('invoice_date','>=',data['form']['start']),('invoice_date','<=',data['form']['end']),('type','=','out_invoice')])
        result = []
        for bill in policies_bill:
            for inv in policies_invoice:
                if bill.policy_id.id == inv.policy_id.id:
                    vals = {
                        'name': inv.name,
                        'bill': bill.amount_total,
                        'invoice': inv.amount_total,
                        'total':inv.amount_total - bill.amount_total,
                    }
            result.append(vals)
        return {
            'doc_model': 'account.move',
            'docs': docids,
            'data': data['form'],
            'result':result,
        }
