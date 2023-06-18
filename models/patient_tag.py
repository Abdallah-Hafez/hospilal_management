# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color_picker = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color_2')