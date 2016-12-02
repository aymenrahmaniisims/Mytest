# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import AccessError, UserError
from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import _, api, fields, models
from openerp.exceptions import AccessError, UserError

#Make the week plan as single object
class CateringWeekPlan(models.Model):
    _name = 'catering.week.plan'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    #Get the current employee
    def _employee_get(self):
        record = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)])
        if not record:
            raise UserError(_('There is no employee registred for the connected User, Contact The Hr manager.')) 
        else:
            return record[0]
        
    #Get the current project related to the current employee
    def _employee_project(self):
        record_employee= self._employee_get()
        if not record_employee:
            raise UserError(_('There is no project define for the current employee, Contact the HR manager.')) 
        else:
            return record_employee.project_id.id
    
    
    name = fields.Char(string='Food Plan Name' , required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, store=True, default=_employee_get)
    project_id = fields.Many2one('project.project', string='Project', readonly=True, store=True, default=_employee_project)
    benificery_word_id = fields.Many2one('catering.hospital.benificery.word', string='Benificery Word' , required=True)
    benificery_category_id = fields.Many2one("catering.hospital.benificery.category", related='benificery_word_id.benificery_category_id', string="Benificery Category", readonly=True)
    state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')],
                                    string='State',default='inactive')
    
    #Each object will be with this structure "day_food_session_lines 
    sunday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_breakfast_product_pack',)
    sunday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_breakfast_snack_product_pack',)
    sunday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_dinner_product_pack',)
    sunday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_dinner_snack_product_pack',)
    sunday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_lunch_product_pack',)
    sunday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_lunch_snack_product_pack',)
    
    monday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_monday_breakfast_product_pack',)
    monday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_monday_breakfast_snack_product_pack',)
    monday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_monday_dinner_product_pack',)
    monday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_monday_dinner_snack_product_pack',)
    monday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_monday_lunch_product_pack',)
    monday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_sunday_lunch_snack_product_pack',)

    tuesday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_breakfast_product_pack',)
    tuesday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_breakfast_snack_product_pack',)
    tuesday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_dinner_product_pack',)
    tuesday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_dinner_snack_product_pack',)
    tuesday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_lunch_product_pack',)
    tuesday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_lunch_product_pack',)
    tuesday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_tuesday_lunch_snack_product_pack',)

    wednesday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_breakfast_product_pack',)
    wednesday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_breakfast_snack_product_pack',)
    wednesday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_dinner_product_pack',)
    wednesday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_dinner_snack_product_pack',)
    wednesday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_lunch_product_pack',)
    wednesday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_wednesday_lunch_snack_product_pack',)

    thursday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_breakfast_product_pack',)
    thursday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_breakfast_snack_product_pack',)
    thursday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_dinner_product_pack',)
    thursday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_dinner_snack_product_pack',)
    thursday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_lunch_product_pack',)
    thursday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_thursday_lunch_snack_product_pack',)

    
    friday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_breakfast_product_pack',)
    friday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_breakfast_snack_product_pack',)
    friday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_dinner_product_pack',)
    friday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_dinner_snack_product_pack',)
    friday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_lunch_product_pack',)
    friday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_friday_lunch_snack_product_pack',)


    saturday_breakfast_lines   = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_breakfast_product_pack',)
    saturday_breakfast_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_breakfast_snack_product_pack',)
    saturday_dinner_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_dinner_product_pack',)
    saturday_dinner_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_dinner_snack_product_pack',)
    saturday_lunch_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_lunch_product_pack',)
    saturday_lunch_snack_lines = fields.Many2many(comodel_name = 'product.pack', relation='table_saturday_lunch_snack_product_pack',)

    # we will use them later in the control 
    @api.multi
    def action_activate(self):
        self.write({'state': 'active'})
        
    @api.multi
    def action_inactivate(self):
        self.write({'state': 'inactive'})