# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from odoo import models, fields, api


class ImportSoftwareWizard(models.TransientModel):
    _name = 'import.software.wizard'

    software_ids = fields.Many2many('product.software', string='Software')
    product_ids = fields.Many2many('product.template', string='Devices',
                                   domain=[('categ_type', '=', 'hardware')])

    @api.multi
    def button_generate(self):
        for record in self:
            Psoftware = self.env['product.software']
            for software in record.software_ids:
                for product in record.product_ids:
                    vals = {
                        'product_template_id': product.id,
                        'product_id': software.product_id.id,
                        'lisence_key': software.lisence_key,
                                }
                    args = [('product_template_id', '=', product.id),
                            ('product_id', '=', software.product_id.id)]
                    exist = Psoftware.search(args, limit=1)
                    if exist:
                        del vals['product_template_id']
                        del vals['product_id']
                        exist.write(vals)
                    else:
                        Psoftware.create(vals)