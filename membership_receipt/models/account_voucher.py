# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

from datetime import date


class AccountVoucherLine(models.Model):
    _inherit = 'account.voucher.line'

    @api.multi
    def write(self, vals):
        MemberLine = self.env['membership.membership_line']
        res = super(AccountVoucherLine, self).write(vals)
        for line in self.filtered(lambda line: line.voucher_id.voucher_type == 'sale'):
            member_lines = MemberLine.search([('account_voucher_line', '=', line.id)])
            if line.product_id.membership and not member_lines:
                # Product line has changed to a membership product
                date_from = line.product_id.membership_date_from
                date_to = line.product_id.membership_date_to
                if (line.voucher_id.date > (date_from or date.min) and
                        line.voucher_id.date < (date_to or date.min)):
                    date_from = line.voucher_id.date
                MemberLine.create({
                    'partner': line.voucher_id.partner_id.id,
                    'membership_id': line.product_id.id,
                    'member_price': line.price_unit,
                    'date': fields.Date.today(),
                    'date_from': date_from,
                    'date_to': date_to,
                    'account_voucher_line': line.id,
                })
            if line.product_id and not line.product_id.membership and member_lines:
                # Product line has changed to a non membership product
                member_lines.unlink()
        return res

    @api.model
    def create(self, vals):
        MemberLine = self.env['membership.membership_line']
        voucher_line = super(AccountVoucherLine, self).create(vals)
        if voucher_line.voucher_id.voucher_type == 'sale' and \
                voucher_line.product_id.membership and \
                not MemberLine.search([('account_voucher_line', '=', voucher_line.id)]):
            # Product line is a membership product
            date_from = voucher_line.product_id.membership_date_from
            date_to = voucher_line.product_id.membership_date_to
            if (date_from and
                    date_from <
                    (voucher_line.voucher_id.date or date.min) <
                    (date_to or date.min)):
                date_from = voucher_line.voucher_id.date
            MemberLine.create({
                'partner': voucher_line.voucher_id.partner_id.id,
                'membership_id': voucher_line.product_id.id,
                'member_price': voucher_line.price_unit,
                'date': fields.Date.today(),
                'date_from': date_from,
                'date_to': date_to,
                'account_voucher_line': voucher_line.id,
            })
        return voucher_line
