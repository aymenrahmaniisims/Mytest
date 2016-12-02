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
from bzrlib.transport import readonly
import calendar

class CateringDietOrder(models.Model):
    _name = 'catering.diet.order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    #Get the employee related to the current user
    def _employee_get(self):
        record = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)])
        if not record:
            raise UserError(_('There is no employee registred for the connected User, Contact The Hr manager.')) 
        else:
            return record[0]
        
    #get the project related to the current employee
    def _employee_project(self):
        record_employee= self._employee_get()
        if not record_employee:
            raise UserError(_('There is no project define for the current employee, Contact the HR manager.')) 
        else:
            return record_employee.project_id.id
    
    name = fields.Char('Order Reference', readonly=True, required=True, index=True, copy=False, default='New')
    #project_id = fields.Many2one('project.project', string='Project', required=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True, store=True, default=_employee_project)
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, store=True, default=_employee_get)
    food_session = fields.Selection([('breakfast', 'BreakFast'), ('breakfast_snack', 'breakfast_snack'),
                                     ('lunch', 'Lunch'),('Lunch_Snack', 'Lunch_Snack'),
                                     ('dinner', 'Dinner'),('Dinner_Snack', 'Dinner_Snack')
                                     ],string='Food Session', required=True,track_visibility='always', help="Food session.")
    order_date = fields.Datetime(string='Order Date', required=True, default=fields.Datetime.now)
    day = fields.Char(string='Day',readonly=True)
    state = fields.Selection([('draft', 'draft'), ('confirm', 'confirmed'),
                                     ('done', 'done'),('cancel', 'Cancelled'),
                                     ],
                                    string='State',default='draft')
    #Fields used to track the visibilty of some field and button on the view
    track_generate_food_plans = fields.Boolean(string='track_generate_food_plans')
    track_generate_required_pack = fields.Boolean(string='track_generate_required_pack')
    track_generate_required_products = fields.Boolean(string='track_generate_required_products')
    
    #Created from the current employee project
    diet_order_lines = fields.One2many('diet.order.line', 'diet_order_id', 'Diet Order Lines')
    #Generated from the week plan and the current project word
    diet_product_pack_lines = fields.One2many('diet.order.pack.line', 'diet_order_id', 'Product Pack Lines')
    #Generated from the pack lines structure
    diet_product_product_lines = fields.One2many('diet.order.product.line', 'diet_order_id', 'BOM Lines')
    
    
    #Generate the sequence number of the diet order
    #The sequence number should be based on project cod(will fix it later)
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('catering.diet.order') or '/'
        return super(CateringDietOrder, self).create(vals)

    #Generate the food plans from the project configuration
    @api.multi
    def generate_food_plans(self):
        if self.project_id and self.project_id.benificery_word_ids and self.order_date:
            object_date= datetime.strptime(self.order_date, "%Y-%m-%d %H:%M:%S")
            self.day=object_date.strftime("%A")
            for benificery_word in self.project_id.benificery_word_ids:
                result = {
                            'benificery_word_id': benificery_word.id,
                            'benificery_word_category_id': benificery_word.benificery_category_id.id,
                            'project_id': self.project_id.id,
                            'diet_order_id': self.id,
                            'number_of_benificery': 0,
                        }
                #Create the order lines
                self.env['diet.order.line'].create(result)
            self.track_generate_food_plans=True
        else:
            raise UserError(_('There is no benificery word define in for this employee project.'))
        
    #Generate the required pack based on the order lines 
    @api.multi
    def generate_required_pack(self):
        if self.project_id and self.diet_order_lines and self.food_session and self.order_date:
            self.track_generate_required_pack=True
            
            #For each line get the week plan and apply it 
            for diet_order_line in self.diet_order_lines:
                if diet_order_line.number_of_benificery >0:
                    week_plans = self.env['catering.week.plan'].search ([
                                ('benificery_word_id', '=', diet_order_line.benificery_word_id.id),
                                ('benificery_category_id', '=', diet_order_line.benificery_word_category_id.id),
                                ('project_id', '=', diet_order_line.project_id.id),
                            ])
                    #the object_week_food should be with the some structure on the week plan "day_food_session_lines"
                    obj_week_food= (self.day+"_"+self.food_session+"_lines").lower()
                    for week_plan in week_plans:
                        for prod_pack in getattr(week_plan, obj_week_food):
                            result = {
                                'project_id': self.project_id.id,
                                'diet_order_id': self.id,
                                'required_quantity': diet_order_line.number_of_benificery,
                                'confirmed_quantity': diet_order_line.number_of_benificery,
                                'product_pack_ids': prod_pack.id,
                            }
                            #create pack lines
                            self.env['diet.order.pack.line'].create(result)
                    diet_order_line.line_state="Done"
                else:
                    #If there is no benificery
                    diet_order_line.line_state="Number Benificery= 0"
                    
    #Generate the required products based on the confirmed number of pack
    @api.multi
    def generate_required_products(self):
        if self.diet_product_pack_lines:
            self.track_generate_required_products=True
            #Get the required product from the 
            for product_pack_line in self.diet_product_pack_lines:
                if product_pack_line.confirmed_quantity >0:
                    for basic_product_pack in product_pack_line.product_pack_ids.basic_product_pack_lines:
                        result = {
                                'project_id': self.project_id.id,
                                'diet_order_id': self.id,
                                'product_id': basic_product_pack.product_id.id,
                                'product_uom': basic_product_pack.product_uom.id,
                                'required_quantity': basic_product_pack.product_uom_qty * product_pack_line.confirmed_quantity,
                            }
                        self.env['diet.order.product.line'].create(result)
                    for support_product_pack in product_pack_line.product_pack_ids.support_product_pack_lines:
                        result = {
                                'project_id': self.project_id.id,
                                'diet_order_id': self.id,
                                'product_id': support_product_pack.product_id.id,
                                'product_uom': support_product_pack.product_uom.id,
                                'required_quantity': support_product_pack.product_uom_qty * product_pack_line.confirmed_quantity,
                            }
                        self.env['diet.order.product.line'].create(result)
    

    
    #Change the state to confirmed
    @api.multi
    def action_confirm(self):
        #Hide the necessary field in the view
        self.write({'state': 'confirm'})
    
    #Change the state to done    
    @api.multi
    def action_done(self):
        #Hide the necessary field in the view
        self.write({'state': 'done'})
    
    #Change the state to cancel
    @api.multi
    def action_cancel(self):
        #Make disable for the edit
        #Hide the necessary field in the view
        #Cancel, or remove the related object
        self.write({'state': 'cancel'})    

#Diet order line generated from the project config
class DietOrderLine(models.Model):
    _name = 'diet.order.line'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    diet_order_id = fields.Many2one('catering.diet.order', "Diet order")
    benificery_word_id = fields.Many2one('catering.hospital.benificery.word', "Benificery Word")
    benificery_word_category_id = fields.Many2one('catering.hospital.benificery.category', "Benificery Category")
    project_id = fields.Many2one('project.project', string='Project')
    number_of_benificery = fields.Integer(string= 'Number Of Benificery', default=0)
    line_state = fields.Char(string= 'Line state', readonly=True)
    note = fields.Char(string= 'Note')
    
    @api.constrains('number_of_benificery')
    def _number_of_benificery_constrains(self):
        if self.number_of_benificery<0:
            raise Warning(_('The Number of benificery must be greater than Zero.'))
            
#Diet required pack generated from the order lines 
class DietOrderPackLine(models.Model):
    _name = 'diet.order.pack.line'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    project_id = fields.Many2one('project.project', string='Project')
    diet_order_id = fields.Many2one('catering.diet.order', "Diet order")
    product_pack_ids = fields.Many2one('product.pack', "Product Pack")
    required_quantity = fields.Integer("Required Quantity", default=0)
    confirmed_quantity = fields.Integer(string= 'Confirmed Quantity', default=0)
    line_state = fields.Integer(string= 'Line state', readonly=True)
    note = fields.Char(string= 'Note')
    
    @api.constrains('required_quantity')
    def _required_quantity_constrains(self):
        if self.required_quantity<0:
            raise Warning(_('The required_quantity must be greater than Zero.'))
        
    @api.constrains('confirmed_quantity')
    def _confirmed_quantity_constrains(self):
        if self.confirmed_quantity<0:
            raise Warning(_('The confirmed_quantity must be greater than Zero.'))

#List of required products generated based on the pack lines  
class DietOrderProductLine(models.Model):
    _name = 'diet.order.product.line'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    diet_order_id = fields.Many2one('catering.diet.order', "Diet order")
    project_id = fields.Many2one('project.project', string='Project')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    product_image = fields.Char(string='Product Image')
    required_quantity = fields.Float(string='Required Quantity', digits=dp.get_precision('Product Unit of Measure'))
    confirmed_quantity = fields.Float(string='Confirmed Quantity', digits=dp.get_precision('Product Unit of Measure'))
    note = fields.Char(string= 'Note')
    
    @api.constrains('required_quantity')
    def _required_quantity_constrains(self):
        if self.required_quantity<0:
            raise Warning(_('The required_quantity must be greater than Zero.'))
        
    @api.constrains('confirmed_quantity')
    def _confirmed_quantity_constrains(self):
        if self.confirmed_quantity<0:
            raise Warning(_('The confirmed_quantity must be greater than Zero.'))
    
    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0
        self.update(vals)
        return {'domain': domain}

   