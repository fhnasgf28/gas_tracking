from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_store = fields.Boolean(string='Is Store', default=False)
