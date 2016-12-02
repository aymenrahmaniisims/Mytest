# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import AccessError, UserError
from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    #List of benificery category in the hospital 
    benificery_word_ids = fields.One2many('catering.hospital.benificery.word', 'project_id', 'Benificery Word')
    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    
    
class CateringHospitalBenificeryWord(models.Model):
    _name = 'catering.hospital.benificery.word'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    #Get the current employee related to the current user
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
    
    name = fields.Char('Name', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, store=True, default=_employee_get)
    project_id = fields.Many2one('project.project', string='Project', readonly=True, store=True, default=_employee_project)
    benificery_category_id = fields.Many2one('catering.hospital.benificery.category', string='Benificery Category')
    
    _sql_constraints = [
        ('name_uniq', 'unique(name,project_id,benificery_category_id)', 'This patient word it-s already created !!')
    ]

#benificery category as fixed in the contract (normal , child ...
class CateringHospitalBenificeryCategory(models.Model):
    _name = 'catering.hospital.benificery.category'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(string='Category Name', required=True)
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This Benificery Category  it-s already created !!')
    ]
    
#Product pack to be built in the week plan (Basic and support product will be added on the pack
class ProductPack(models.Model):
    _name = 'product.pack'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _employee_get(self):
        record = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)])
        if not record:
            raise UserError(_('There is no employee registred for the connected User, Contact The Hr manager.')) 
        else:
            return record[0]
    
    def _employee_project(self):
        record_employee= self._employee_get()
        if not record_employee:
            raise UserError(_('There is no project define for the current employee, Contact the HR manager.')) 
        else:
            return record_employee.project_id.id
    
    
    name = fields.Char(string='Pack Name', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, store=True, default=_employee_get)
    project_id = fields.Many2one('project.project', string='Project', readonly=True, store=True, default=_employee_project)
    basic_product_pack_lines = fields.One2many('basic.product.product', 'product_pack_id', 'Basic Product')
    support_product_pack_lines = fields.One2many('support.product.product', 'product_pack_id', 'Support product')

class BasicProductProduct(models.Model):
    _name = 'basic.product.product'
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    product_image = fields.Char(string='Product Image')
    product_after_before_cooking = fields.Float(string='+-/100 Cooking')
    note = fields.Char(string='Note')
    product_pack_id = fields.Many2one('product.pack', string='product Pack')
    
    @api.constrains('product_uom_qty')
    def _product_uom_qty_constrains(self):
        if self.product_uom_qty<0:
            raise Warning(_('The product_uom_qty must be greater than Zero.'))
        
    
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



class SupportProductProduct(models.Model):
    _name = 'support.product.product'
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    product_image = fields.Char(string='Product Image')
    product_after_before_cooking = fields.Float(string='+-/100 Cooking')
    note = fields.Char(string='Note')
    product_pack_id = fields.Many2one('product.pack', string='product Pack')
    
    @api.constrains('product_uom_qty')
    def _product_uom_qty_constrains(self):
        if self.product_uom_qty<0:
            raise Warning(_('The product_uom_qty must be greater than Zero.'))
    
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


