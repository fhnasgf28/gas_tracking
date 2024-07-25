from odoo import models

class PurchaseOrderWizardXlsx(models.AbstractModel):
    _name = 'report.purchase_order_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, the_report):
        obj = data['the_report']
        sheet = workbook.add_worksheet('Purchase Order Data')
        
        # Format with bold text and yellow background
        header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})

        # Write the headers
        sheet.write('A1', 'Vendor', header_format)
        sheet.write('B1', 'Order Deadline Date', header_format)
        sheet.write('C1', 'Amount Total', header_format)
        sheet.write('D1', 'Duration', header_format)
        sheet.write('E1', 'Product', header_format)
        sheet.write('F1', 'Price Unit', header_format)
        sheet.write('G1', 'Quantity', header_format)
        sheet.write('H1', 'Subtotal', header_format)

        row = 1
        total_duration = 0
        total_amount_total = 0
        num_orders = len(obj)

        for x in obj:
            col = 0
            sheet.write(row, col, x['partner_id'][1])
            col += 1
            sheet.write(row, col, x['date_order'])
            col += 1
            sheet.write(row, col, x['amount_total'])
            total_amount_total += x['amount_total']
            col += 1
            sheet.write(row, col, x['duration'])
            total_duration += x['duration']
            col += 1

            # Fetch details of each order line
            for detail_id in x['order_line']:
                detail = self.env['purchase.order.line'].browse(detail_id)

                # Write detail fields
                sheet.write(row, col, detail.product_id.name)
                col += 1
                sheet.write(row, col, detail.price_unit)
                col += 1
                sheet.write(row, col, detail.product_qty)
                col += 1
                sheet.write(row, col, detail.price_subtotal)
                col += 1
                row += 1  
                col = 3  

            if not x['order_line']:
                row += 1

        # Calculate the average duration
        average_duration = total_duration / num_orders if num_orders > 0 else 0

        # Write the totals and average duration at the end
        sheet.write(row, 0, 'Total', header_format)
        sheet.write(row, 2, total_amount_total, header_format)
        sheet.write(row, 3, total_duration, header_format)
        row += 1
        sheet.write(row, 0, 'Average Duration', header_format)
        sheet.write(row, 3, average_duration, header_format)
