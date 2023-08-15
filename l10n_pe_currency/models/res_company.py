#######################################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
#######################################################################################

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_pe_exchange_rate_validation = fields.Boolean(string="Exchange Rate Validation")

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = super(ResCompany, self)._onchange_country_id()
        if self.country_id and self.country_id.code == "PE":
            self.l10n_pe_exchange_rate_validation = True
        else:
            self.l10n_pe_exchange_rate_validation = False
        return res
