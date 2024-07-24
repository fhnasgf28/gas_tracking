from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    responsible_for_cylinders = fields.One2many(
        'gas.transaction', 
        'employee_id', 
        string='Responsible Cylinders'
    )