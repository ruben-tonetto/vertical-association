from odoo import api, models, _
from odoo.exceptions import UserError


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def create_membership_receipt(self, product_id=None, datas=None):
        product_id = product_id or datas.get('membership_product_id')
        amount = datas.get('amount', 0.0)
        receipt_list = []
        product = self.env['product.product'].browse(product_id)
        for partner in self:
            addr = partner.address_get(['invoice'])
            if partner.free_member:
                raise UserError(_("Partner is a free Member."))
            if not addr.get('invoice', False):
                raise UserError(
                    _("Partner doesn't have an address to make the receipt.")
                )
            receipt = self.env['account.voucher'].create({
                'partner_id': partner.id,
                'account_id': partner.property_account_receivable_id.id,
                'fiscal_position_id': partner.property_account_position_id.id,
                'voucher_type': 'sale'
            })
            line_values = {
                'product_id': product_id,
                'price_unit': amount,
                'receipt_id': receipt.id,
                'name': product.partner_ref,
                'account_id': partner.property_account_receivable_id.id,
            }
            # create a record in cache, apply onchange then revert back to a dictionary
            receipt_line = self.env['account.voucher.line'].new(line_values)
            receipt_line._onchange_line_details()
            line_values = receipt_line._convert_to_write({
                name: receipt_line[name] for name in receipt_line._cache
            })
            line_values['price_unit'] = amount
            receipt.write({'line_ids': [(0, 0, line_values)]})
            receipt_list.append(receipt.id)
        return receipt_list
