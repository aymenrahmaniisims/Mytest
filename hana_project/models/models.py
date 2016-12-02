# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import AccessError, UserError

class res_user(models.Model):
    _inherit = 'res.users'
    
    project_id = fields.Many2one('project.project', string='Project')

class hr_employee(models.Model):
    _inherit = 'hr.employee'
    
    project_id = fields.Many2one("project.project", related='user_id.project_id', string="Project", readonly=True)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    code = fields.Char( string='Project Code', required=True, default="/", readonly=True)
    region_id = fields.Many2one('ksa.region', string='Region')
    city_id = fields.Many2one('ksa.city', string='City')
    #project_category_id = fields.Many2one('projectategory', string='Category')
    

    _sql_constraints = [
        ('project_unique_code', 'UNIQUE (code)', _('The code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        #The code should be with this structure Date_start/Category/sequence_number/Date_End
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].get('project.project')
        return super(ProjectProject, self).create(vals)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].get('project.project')
        return super(ProjectProject, self).copy(default)