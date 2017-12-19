# -*- coding: utf-8 -*-
# © 2017 Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_type = fields.Selection(
        [('percent', 'Percentual'),
         ('amount', 'Quantia')],
        string='Tipo de Desconto',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]},
        default='percent')

    discount_value = fields.Float(
        string='Desconto',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]})

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self.update_discount_lines()
        return res

    @api.multi
    def update_discount_lines(self):
        for item in self:
            if item.discount_value == 0:
                continue
            discount_percent = item.discount_value
            if item.discount_type == 'amount':
                discount_percent = item.discount_value / item.total_bruto * 100
            if discount_percent > 100:
                discount_percent = 100
            elif discount_percent < 0:
                discount_percent = 0
            for line in item.order_line:
                line.discount = discount_percent