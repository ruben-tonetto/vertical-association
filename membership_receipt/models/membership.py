# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MembershipLine(models.Model):
    _inherit = 'membership.membership_line'

    account_voucher_line = fields.Many2one('account.voucher.line',
                                           string='Account Receipt Line',
                                           readonly=True, ondelete='cascade')
    account_voucher_id = fields.Many2one('account.voucher',
                                         related='account_voucher_line.voucher_id',
                                         string='Receipt', readonly=True)
