{
    'name': 'Website Versioning',
    'category': 'Website',
    'summary': 'Keep all the versions of your website',
    'version': '1.0',
    'description': """
OpenERP Website CMS
===================

        """,
    'author': 'OpenERP SA',
    'depends': ['website'],
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/website_backend_navbar.xml',
        'views/website_version_templates.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'application': True,
}