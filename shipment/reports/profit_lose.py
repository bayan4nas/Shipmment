from odoo import api, models,fields,  _


class ProfitReport(models.AbstractModel):
    _name = 'report.shipment.profit_lose_report'
    _description = 'Profit & Lose Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        start = data['form']['start']
        end = data['form']['end']
        domain = [('invoice_date','>=',start),('invoice_date','<=',end)]
        if data['form']['policy_ids']:
            domain += [('policy_id','in',data['form']['policy_ids'])]

        moves = self.env['account.move'].search(domain)
        in_invoice = moves.filtered(lambda i: i.type == 'in_invoice')
        out_invoice = moves.filtered(lambda i: i.type == 'out_invoice')

        """as one policy could have more than customer invoice,
        so we take ploicy from report wizard and get the moves for ,
         both in and out invoices see above two lines
         then iterate for the bill and get all the related invocies ,
         related invoices are known if bill and in_invoice have the same policy_id,
         the we sum amount total for all related invoices 
         so we have single dic contains bill amount and sum of related invocies to be printed"""
         
        move_list = []
        for invoi in in_invoice:
            total = 0.0
            for ouinv in out_invoice:
                if invoi.policy_id == ouinv.policy_id and not invoi.commission:
                    
                    total+= ouinv.amount_total

            vals = {
                'currency':invoi.currency_id.id,
                'name': invoi.policy_id.name,
                'bill': invoi.amount_total,
                'commission':invoi.amount_total if invoi.commission else 0.0,
                'company':invoi.partner_id.name,
                'invoice':total,
                'invoice_date':invoi.invoice_date,
                'diff':invoi.amount_total - total,
            }
            move_list.append(vals)
       
        return {
            'doc_model': 'account.move',
            'docs': docids,
            'data': data['form'],
            'result':move_list,
        }
