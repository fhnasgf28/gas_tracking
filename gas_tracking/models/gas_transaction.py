from odoo import models, fields, api, exceptions
from datetime import timedelta

class GasTransaction(models.Model):
    _name = 'gas.transaction'
    _description = 'Gas Transaction'

    product_id = fields.Many2one('product.product', string='Gas Product', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    transaction_date = fields.Date(string='Transaction Date', default=fields.Date.context_today)
    due_date = fields.Date(compute='_compute_due_date', string='Due Date', store=True)
    default_code = fields.Char(related='product_id.default_code', string='Serial Number', readonly=True)
    last_refill_date = fields.Date(related='product_id.last_refill_date', string='Last Refill Date', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Staff')
    transaction_state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('empty', 'Empty'),
        ('done', 'Done'),
    ], string='Transaction State', compute='_compute_transaction_state', store=True, default='available')

    profit = fields.Float(compute='_compute_profit', string='Profit', store=True)

    @api.depends('product_id')
    def _compute_profit(self):
        for record in self:
            record.profit = record.product_id.list_price if record.transaction_state == 'done' else 0.0

    @api.model
    def create(self, vals):
        record = super(GasTransaction, self).create(vals)
        # Check if the transaction_state should be set to 'in_use'
        if record.product_id:
            record.product_id.write({'state': 'in_use'})
            record.write({'transaction_state': 'in_use'})
        return record

    @api.depends('product_id')
    def _compute_transaction_state(self):
        for record in self:
            state = record.product_id.state
            if state in ['in_use', 'empty', 'available']:
                record.transaction_state = state
            else:
                record.transaction_state = 'available'

    @api.depends('transaction_date')
    def _compute_due_date(self):
        for record in self:
            if record.transaction_date:
                transaction_date = fields.Date.from_string(record.transaction_date)
                due_date = transaction_date + timedelta(days=7)
                record.due_date = fields.Date.to_string(due_date)
            else:
                record.due_date = False

    def return_cylinder(self):
        self.ensure_one()
        if self.transaction_state == 'in_use':
            self.product_id.write({'state': 'empty'})
            self.write({'transaction_state': 'empty'})
        else:
            raise exceptions.UserError('Cylinder is not in use.')

    def refill_cylinder(self):
        self.ensure_one()
        if self.transaction_state == 'empty':
            self.product_id.write({'state': 'available'})
            self.write({'transaction_state': 'done'})
        else:
            raise exceptions.UserError('Cylinder is not empty.')

    def unlink(self):
        # Overriding unlink to handle specific conditions
        for record in self:
            if record.transaction_state == 'done':
                raise exceptions.UserError("You cannot delete records with state 'Done'.")
        return super(GasTransaction, self).unlink()

