from odoo import models, fields, api

class GasProduct(models.Model):
    _inherit = 'product.template'
    
    employee_id = fields.Many2one('hr.employee', string='Staff')
    name = fields.Char(string='Product Name', required=True)
    default_code = fields.Char(string='Serial Number', required=True, unique=True)
    last_refill_date = fields.Date(string='Last Refill Date', readonly=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('empty', 'Empty'),
    ], string='Status', default='available')

    transaction_ids = fields.Many2one(comodel_name='gas.transaction', string='Due Date')
    product_template_attribute_value_ids = fields.Many2many(comodel_name='product.template.attribute.value', string='id')
    product_tmpl_id = fields.One2many(comodel_name='product.product', inverse_name='product_variant_id', string='id')
    

    @api.model
    def create(self, vals):
        # Set the default value for last_refill_date if the state is empty
        if vals.get('state') == 'empty':
            vals['last_refill_date'] = fields.Date.today()
        return super(GasProduct, self).create(vals)

    def write(self, vals):
        # Check if the state is being changed to empty
        if 'state' in vals and vals['state'] == 'empty':
            vals['last_refill_date'] = fields.Date.today()
        return super(GasProduct, self).write(vals)