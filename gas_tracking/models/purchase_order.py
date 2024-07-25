from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    duration = fields.Float(
        compute='action_compute_duration',
        string='Duration (days)',
        readonly=True,
        default=0.0,
        help='Number of days from PO creation to payment',
    )
    partner = fields.Many2one(comodel_name='res.partner', string='partner')
    
    # Method to compute duration when payment is done

    def action_compute_duration(self):
        for order in self:
            if order.date_order and order.date_approve:
                start_date = fields.Datetime.from_string(order.date_order)
                end_date = fields.Datetime.from_string(order.date_approve)
                duration_days = (end_date - start_date).days
                order.duration = duration_days
            else:
                order.duration = 0.0



# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#     _description = 'PurchaseOrderLine'

    
#     duration_line = fields.Float(
#         # compute='action_compute_duration_line',
#         string='Duration (days)',
#         readonly=True,
#         default=0.0,
#         help='Number of days from PO creation to payment',
#         store=True,
#     )

    # def action_compute_duration(self):
    #     for order in self:
    #         if order.date_order and order.date_approve:
    #             start_date = fields.Datetime.from_string(order.date_order)
    #             end_date = fields.Datetime.from_string(order.date_approve)
    #             duration_days = (end_date - start_date).days
    #             order.duration = duration_days
    #         else:
    #             order.duration = 0.0


