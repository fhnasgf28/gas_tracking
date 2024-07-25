from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    data_order = fields.One2many(
        'gas.transaction', 
        'customer_id', 
        string='Data Order'
    )

    purchase_order = fields.One2many(comodel_name='purchase.order', inverse_name='partner_id', string='Purchase')
    