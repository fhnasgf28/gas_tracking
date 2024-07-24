from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    data_order = fields.One2many(
        'gas.transaction', 
        'customer_id', 
        string='Data Order'
    )