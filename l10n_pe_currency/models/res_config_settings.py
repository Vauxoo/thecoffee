#######################################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
#######################################################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_pe_exchange_rate_validation = fields.Boolean(
        string="Exchange Rate Validation",
        related="company_id.l10n_pe_exchange_rate_validation",
        readonly=False,
    )
