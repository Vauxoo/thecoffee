from odoo import api, fields, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    _sql_constraints = [
        ('unique_name', 'CHECK(1=1)','Error Message'),
        ('unique_type_name', 'unique (name,rate_type)',
         'The currency code already exists in this rate type!'),
        ('rounding_gt_zero', 'CHECK (rounding>0)',
         'The rounding factor must be greater than 0!')
    ]
    
    rate_type = fields.Selection([
        ('purchase', 'Compra'),
        ('sale', 'Venta'),
    ], string='Tipo de cambio')

    def name_get(self):
        res = []
        for currency in self:
            if currency.rate_type:
                if currency.rate_type == 'sale':
                    rate_type = 'Venta'
                else:
                    rate_type = 'Compra'
                complete_name = '%s/%s ' % (currency.name, rate_type)
            else:
                complete_name = currency.name
            res.append((currency.id, complete_name))
        return res
