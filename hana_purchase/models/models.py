# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import AccessError, UserError
from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class PeriodicallyPurchaseOrder(models.Model):
    _name = 'periodically.purchase.order'
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
    
    
    name = fields.Char(string='Reference', required=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, store=True, default=_employee_get)
    project_id = fields.Many2one('project.project', string='Project', readonly=True, store=True, default=_employee_project)
    date_order = fields.Datetime('Order Date', required=True, index=True, copy=False, default=fields.Datetime.now,\
        help="Depicts the date where the Quotation should be validated and converted into a purchase order.")
    date_approve = fields.Date('Approval Date', readonly=1, index=True, copy=False)
    date_planned = fields.Datetime(string='Scheduled Date', required=True)

    
    
    order_lines = fields.One2many('periodically.purchase.order.line', 'periodically_purchase_order_id', 'Order Lines')
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('periodically.purchase.order') or '/'
        return super(PeriodicallyPurchaseOrder, self).create(vals)
    
    @api.multi
    def do_merge(self):
        #Use this function to merge many orders in one in order to generate single PO
        
        return True

#The purchase employee should be able later to merge many sites order in one and choose the supplier then generate the PO    
class PeriodicallyPurchaseOrderLine(models.Model):
    _name = 'periodically.purchase.order.line'
    
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    product_image = fields.Char(string='Product Image')
    note = fields.Char(string='Note')
    priority =  fields.Selection([('Normal', 'Normal'),('Low', 'Low'), ('High', 'High'),('Very_High', 'Very High')],string='Rating', select=True)
    periodically_purchase_order_id = fields.Many2one('periodically.purchase.order', string='Periodically Purchase Order')
    
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

    
        return True
