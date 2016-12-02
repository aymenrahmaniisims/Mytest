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

class KsaRegion(models.Model):
    _description = "KSA region"
    _name = 'ksa.region'
    
    name= fields.Char('Region Name', size=64, required=True, select=True, help='Administrative region of a state.')
    code = fields.Char('Code', size=64, required=True, select=True, help='Region Code.')
    country_id =  fields.Many2one('res.country', 'Country', required=True, ondelete='cascade', select=True,)

class KsaCity(models.Model):
    _description = "KSA city"
    _name = 'ksa.city'
    
    name = fields.Char('City Name', size=64, required=True, select=True, help='Administrative City .')
    code = fields.Char('Code', size=64, required=True, select=True, help='City Code.')
    region_id =  fields.Many2one('ksa.region', 'Region', required=True,)


class KsaCityPart(models.Model):
    _description = "KSA city part"
    _name = 'ksa.city.part'
    
    name = fields.Char('City part Name', size=64, required=True, select=True, help='Administrative City Part .')
    code = fields.Char('Code', size=64, required=True, select=True, help='City Part Code.')
    city_id =  fields.Many2one('ksa.city', 'City Part', required=True,)
