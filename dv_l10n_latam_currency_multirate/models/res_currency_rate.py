from odoo import models, fields, api


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    currency_name = fields.Char(related='currency_id.name', store=True)
    currency_rate_type = fields.Selection(
        related='currency_id.rate_type', store=True)
    currency_display_name = fields.Char(
        related='currency_id.display_name', store=True)
