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


class ResCurrency(models.Model):
    _inherit = "res.currency"

    remote_id = fields.Char(string="Remote ID")

    @api.model
    def fetch_exchange_rate_data(self, company, type_consult, currency):
        user_token = self.env["iap.account"].get("l10n_pe_data")
        dbuuid = self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        data = {}
        params = {
            "client_service_token": company.l10n_pe_partner_token,
            "remote_id": currency.remote_id,
            "account_token": user_token.account_token,
            "doc_number": "",
            "type_consult": type_consult,
            "currency": currency.name,
            "company_name": company.name,
            "phone": company.phone,
            "email": company.email,
            "service": "partner",
            "company_image": company.logo.decode("utf-8"),
            "number": company.vat,
            "dbuuid": dbuuid,
        }
        rate = self.connect_to_iap("/iap/get_partner_data", params)
        if rate:
            result = rate["exchange_rates"][0]
            data = self.rate_connection(rate, result, company, currency)
        return data

    @api.model
    def rate_connection(self, rate, result, company, currency):
        data = {}
        try:
            data["company_id"] = company.id
            data["currency_id"] = currency.id
            data["name"] = fields.Date.today()
            data["inverse_company_rate"] = result.get("venta")

            rate_line = self.env["res.currency.rate"].search(
                [
                    ("company_id", "=", company.id),
                    ("currency_id", "=", currency.id),
                    ("name", "=", fields.Date.today()),
                ],
                limit=1,
            )

            if rate_line:
                rate_line.write(data)
            else:
                rate_line = self.env["res.currency.rate"].create(data)
                currency.remote_id = rate.get("remote_id", False)
        except Exception:
            data = False

        return data

    @api.model
    def l10n_pe_exchange_rate_connection(self):
        currency_rate = self.env["res.currency.rate"].search(
            [("name", "=", fields.Date.today())]
        )
        if not currency_rate:
            usd_currency = self.env["res.currency"].search(
                [("name", "=", "USD")], limit=1
            )
            if usd_currency:
                companies = self.env["res.company"].search(
                    [("currency_id.name", "=", "PEN")]
                )
                for company in companies:
                    if company.l10n_pe_exchange_rate_validation:
                        if company.l10n_pe_partner_token:
                            type_consult = "exchange_rate_consult"
                            currency = usd_currency
                            return self.fetch_exchange_rate_data(
                                company, type_consult, currency
                            )
        return {}
