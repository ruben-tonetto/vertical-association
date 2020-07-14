# Copyright 2020 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Membership Receipt',
    'version': '12.0.1.0.0',
    'category': 'Vertical Association',
    'summary': 'Enable membership receipt',
    'author': 'Pordenone Linux User Group (PNLUG), Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/vertical-association',
    'license': 'AGPL-3',
    'depends': [
        'membership',
        'account_voucher'],
    'data': [
        'views/membership_receipt_views.xml',
        'views/partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
