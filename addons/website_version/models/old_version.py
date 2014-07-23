# -*- coding: utf-8 -*-

import collections
import copy
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
import fnmatch
import logging
import os
import time
from operator import itemgetter

import simplejson
import werkzeug
import HTMLParser
from lxml import etree

import openerp
from openerp import tools, api
from openerp.http import request
from openerp.osv import fields, osv, orm
from openerp.tools import graph, SKIPPED_ELEMENT_TYPES
from openerp.tools.parse_version import parse_version
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.view_validation import valid_view
from openerp.tools import misc
from openerp.tools.translate import _


class old_version(osv.osv):
    _name = "website_version.old"
    
    _columns = {
        'arch': fields.text('View Architecture', required=True),
        'view_id': fields.many2one('ir.ui.view',string="Source View"),
    }