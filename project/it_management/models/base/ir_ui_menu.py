# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import SUPERUSER_ID
from odoo import api, fields, models, tools


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        """
        Hide menus needn't use in each profies
        """
        current_user = self.env.user
        res = super(IrUiMenu, self)._visible_menu_ids(debug)

        # ignore SUPERUSER
        if self.env.uid != SUPERUSER_ID:
            menu_to_hide_ids = []
            if current_user.has_group('it_management.group_it_security_admin_limit'):
                menu_to_hide_ids = [
                    self.env.ref('it_management.report_issue_menu_root').id,
                    self.env.ref('it_management.network_menu_root').id,
                    self.env.ref('base.menu_management').id,
                    self.env.ref('base.menu_administration').id,
                ]
            elif current_user.has_group('it_management.group_it_user_limit'):
                menu_to_hide_ids = [
                    self.env.ref('mail.mail_channel_menu_root_chat').id,
                    self.env.ref('it_management.network_menu_root').id,
                    self.env.ref('it_management.report_issue_menu_sub_report').id,
                    self.env.ref('it_management.report_issue_menu_customer').id,
                    self.env.ref('it_management.report_issue_menu_product').id,
                ]
            elif current_user.has_group('it_management.group_it_supporter_limit'):
                menu_to_hide_ids = [
                    self.env.ref('base.menu_management').id,
                    self.env.ref('base.menu_administration').id,
                ]
            res = res - set(menu_to_hide_ids)
        return res
