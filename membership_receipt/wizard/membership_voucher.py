from odoo import api, models


class MembershipInvoice(models.TransientModel):
    _inherit = "membership.invoice"

    @api.multi
    def membership_receipt(self):
        if self:
            datas = {
                'membership_product_id': self.product_id.id,
                'amount': self.member_price
            }

        receipt_list = self.env['res.partner'].\
            browse(self._context.get('active_ids')).\
            create_membership_receipt(datas=datas)

        search_view_ref = self.env.ref('account_voucher.view_voucher_filter', False)
        form_view_ref = self.env.ref('account_voucher.view_sale_receipt_form', False)
        tree_view_ref = self.env.ref('account_voucher.view_voucher_tree', False)

        return {
            'domain': [('id', 'in', receipt_list)],
            'name': 'Membership Receipts',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
            'search_view_id': search_view_ref and search_view_ref.id,
        }
