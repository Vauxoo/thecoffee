from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_available_ids = fields.Many2many('res.currency',
                                              compute='_compute_currency_available_ids'
                                              )

    @api.depends('move_type')
    def _compute_currency_available_ids(self):
        for record in self:
            currencies = self.env['res.currency'].search([])
            if record.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                currency_available_ids = currencies.search([('rate_type', '=', 'purchase')])
            elif record.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
                currency_available_ids = self.env['res.currency'].search([('rate_type', '=', 'sale')])
            else:
                currency_available_ids = currencies
            record.currency_available_ids = currency_available_ids
