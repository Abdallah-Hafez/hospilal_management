# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'name'

    name = fields.Char(string='Sequence', default='New')
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='patient')
    gender = fields.Selection(string='Gender', related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference', help="Reference From Patient Record")
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string="Status", default='draft', required=True)
    doctor_id = fields.Many2one(comodel_name='res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')


    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def object_test(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('hospital_manag.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


# ----------------------------  Appointment Pharmacy Lines Model  ------------------------------#

class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', string="Product", required=True)
    price_unit = fields.Float(related='product_id.lst_price')
    quantity = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
