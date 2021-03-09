from odoo import api, models, fields,  _


class ProfitReport(models.AbstractModel):
    _name = 'report.shipment.profit_lose_report'
    _description = 'Profit & Lose Report'

    def get_value(self, data):
        start = data['form']['start']
        end = data['form']['end']
        domain = [('invoice_date', '>=', start), ('invoice_date', '<=', end)]
        if data['form']['policy_ids']:
            domain += [('ref_id', 'in', data['form']['policy_ids'])]
        else:
            policies = self.env['shipment.order'].search([]).ids
            domain += [('ref_id', 'in', policies)]

        moves = self.env['account.move'].search(domain)
        in_invoice = moves.filtered(
            lambda i: i.type == 'in_invoice')
        print("in invoice===============",in_invoice)
        out_invoice = moves.filtered(lambda i: i.type == 'out_invoice')

        """as one policy could have more than customer invoice,
        so we take ploicy from report wizard and get the moves for ,
         both in and out invoices see above two lines
         then iterate for the bill and get all the related invocies ,
         related invoices are known if bill and in_invoice have the same policy_id,
         the we sum amount total for all related invoices 
         so we have single dic contains bill amount and sum of related invocies to be printed"""
        move_list = []
        for invoi in in_invoice.filtered(lambda r : not r.commission):
            coms = moves.filtered(lambda r : r.ref_id.id == invoi.ref_id.id and r.commission)
            
            total = 0.0
            if not invoi.commission:
                for ouinv in out_invoice:
                    if invoi.ref_id == ouinv.ref_id and not invoi.commission:

                        total += ouinv.amount_total

            vals = {
                'currency': invoi.currency_id.id,
                'name': invoi.policy_id.name,
                'bill': invoi.amount_total,
                'commission': sum(coms.mapped('amount_total')),
                'company': invoi.partner_id.name,
                'invoice': total,
                'invoice_date': invoi.invoice_date,
                'diff': total - invoi.amount_total ,
            }
            move_list.append(vals)
        return move_list

    @api.model
    def _get_report_values(self, docids, data=None):

        move_list = self.get_value(data)
        print("pdf value ===============",move_list)

        return {
            'doc_model': 'account.move',
            'docs': docids,
            'data': data['form'],
            'result': move_list,
        }


class AttendancesReportXls(models.AbstractModel):
    _name = 'report.shipment.shipment_order_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, line):
        move_list = self.env[
                'report.shipment.profit_lose_report'].get_value(data)
        print("excel values ===============",move_list)
        commission = data['form']['commission']
        start = data['form']['start']
        end = data['form']['end']
        format1 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'bold': True, 'font_color': '#843c0b', 'bg_color': 'white', })
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', })
        format3 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'center', 'bold': True, 'font_color': 'white','bg_color': 'gray', })
        sheet = workbook.add_worksheet('Shipment Policy')
        sheet.set_column(2, 0, 20)
        sheet.set_column(2, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(2, 3, 20)
        sheet.set_column(2, 4, 20)
        sheet.set_column(2, 5, 20)
        
        start_date = fields.Date.from_string(start)
        end_date = fields.Date.from_string(end)
        sheet.write(0, 1, 'Policy', format3)
        sheet.write(0, 2, 'From', format3)
        sheet.write(0, 3, str(start)[0:10], format3)
        sheet.write(0, 4, 'To', format3)
        sheet.write(0, 5, str(start)[0:10], format3)
        
        
        sheet.write(2, 0, 'name', format1)
        sheet.write(2, 1, 'Vendor Bills', format1)
        sheet.write(2, 2, 'Company', format1)
        sheet.write(2, 3, 'Customer Invoices', format1)
        sheet.write(2, 4, 'Profit And Lose', format1)
        sheet.write(2, 5, 'Profit And Lose', format1)
        
        if commission:
            sheet.write(2, 5, 'Commission', format1)

        for o in move_list:
            c = 4
            bill = 0
            inv = 0
            company_currncey = self.env.user.company_id.currency_id
            sheet.write(c, 0,o['name'] , format2)
           
            if data['form']['currency'] == 'usd':

                amount_currency = self.env['account.move'].compute_currency_without_rate(o['bill'],o['invoice_date'],o.currency_id.id)
                sheet.write(c, 1, amount_currency, format2)
                bill = bill + amount_currency
            if data['form']['currency'] == 'company':

                amount_currency = self.env['account.move'].compute_currency_without_rate(o['bill'],o['invoice_date'],company_currncey.id)
                sheet.write(c, 1, amount_currency, format2)
                bill = bill + amount_currency
                                        
            sheet.write(c, 2, o['company'], format2)

            if data['form']['currency'] == 'usd':
                amount_currency = self.env['account.move'].compute_currency_without_rate(o['invoice'],o['invoice_date'],o.currency_id.id)
                sheet.write(c, 3, amount_currency, format2)
                inv = inv + amount_currency
            if data['form']['currency'] == 'company':

                amount_currency = self.env['account.move'].compute_currency_without_rate(o['invoice'],o['invoice_date'],company_currncey.id)
                sheet.write(c, 3, amount_currency, format2)
                inv = inv + amount_currency

            sheet.write(c, 4, inv - bill, format2)
           
            if commission:
                sheet.write(c, 5, o['commission'], format2)
            c+=1
