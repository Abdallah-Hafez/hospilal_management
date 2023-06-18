# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date Of Birth')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True, store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True, default="male")
    active = fields.Boolean(string='Active', default=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    image = fields.Image(string='Image')
    # New Table - Max 63 Char
    tag_ids = fields.Many2many(comodel_name='patient.tag', relation='hospital_patient_tags_rel',
                               column1='hospital_patient_id', column2='patient_tag_id', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)
    time_to_leave = fields.Date(string='Time To leave')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)


    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     appointment_group = self.env['hospital.appointment'].read_group(domain=[('state', '=', 'done')],
    #                                                                     fields=['patient_id'], groupby=['patient_id'])
    #     for appointment in appointment_group:
    #         patient_id = appointment.get('patient_id')[0]
    #         patient_rec = self.browse(patient_id)
    #         patient_rec.appointment_count = appointment['patient_id_count']
    #         self -= patient_rec
    #     self.appointment_count = 0


    @api.model
    def create(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def name_get(self):
        # patient_list = []
        # for rec in self:
        #     name = f"{rec.ref} {rec.name}"
        #     patient_list.append((rec.id, name))
        return [(rec.id, "[%s] %s" % (rec.ref, rec.name)) for rec in self]

    def action_view_appointment(self):
        return

    def auto_remove_patient(self):
        self.env["hospital.patient"].search([('time_to_leave', '=', date.today())]).write({'active': False})

