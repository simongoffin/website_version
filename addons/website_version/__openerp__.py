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
    'depends': ['website','marketing'],
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/website_version_assets.xml',
        'views/menu.xml',
        'views/marketing_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'application': True,
}