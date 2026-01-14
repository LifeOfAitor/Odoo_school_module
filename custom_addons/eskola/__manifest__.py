{
    'name': "eskola",

    'summary': "Eskola kudeaketa modulua",

    'description': """
Eskola kudeatzeko modulua izango da, non ikasleak, irakasleak eta ikastaroak kudeatu ahal izango diren.
    """,

    'author': "Aitor",
    'website': "https://zubirimanteo.com/eus/",

    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'data/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

