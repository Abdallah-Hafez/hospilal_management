# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['data_cancel'] = date.today()
        print(res)
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string='Reason')
    data_cancel = fields.Date(string='Cancellation')

    def action_cancel(self):
        active = self.env['hospital.appointment'].browse(self._context.get('active_ids'))
        active.state = 'cancel'

