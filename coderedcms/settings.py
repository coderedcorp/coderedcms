import os
from django.conf import settings
from functools import lru_cache


PROJECT_DIR = settings.PROJECT_DIR if getattr(settings, 'PROJECT_DIR') else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
BASE_DIR = settings.BASE_DIR if getattr(settings, 'BASE_DIR') else os.path.dirname(PROJECT_DIR)

DEFAULTS = {
    'PROTECTED_MEDIA_URL': '/protected/',
    'PROTECTED_MEDIA_ROOT': os.path.join(BASE_DIR, 'protected'),
    'PROTECTED_MEDIA_UPLOAD_WHITELIST': [],
    'PROTECTED_MEDIA_UPLOAD_BLACKLIST': ['.sh', '.exe', '.bat', '.ps1', '.app', '.jar', '.py', '.php', '.pl', '.rb'],  # noqa

    'FRONTEND_BTN_SIZE_DEFAULT': '',
    'FRONTEND_BTN_SIZE_CHOICES': (
        ('btn-sm', 'Small'),
        ('', 'Default'),
        ('btn-lg', 'Large'),
    ),

    'FRONTEND_BTN_STYLE_DEFAULT': 'btn-primary',
    'FRONTEND_BTN_STYLE_CHOICES': (
        ('btn-primary', 'Primary'),
        ('btn-secondary', 'Secondary'),
        ('btn-success', 'Success'),
        ('btn-danger', 'Danger'),
        ('btn-warning', 'Warning'),
        ('btn-info', 'Info'),
        ('btn-link', 'Link'),
        ('btn-light', 'Light'),
        ('btn-dark', 'Dark'),
        ('btn-outline-primary', 'Outline Primary'),
        ('btn-outline-secondary', 'Outline Secondary'),
        ('btn-outline-success', 'Outline Success'),
        ('btn-outline-danger', 'Outline Danger'),
        ('btn-outline-warning', 'Outline Warning'),
        ('btn-outline-info', 'Outline Info'),
        ('btn-outline-light', 'Outline Light'),
        ('btn-outline-dark', 'Outline Dark'),
    ),

    'FRONTEND_CAROUSEL_FX_DEFAULT': '',
    'FRONTEND_CAROUSEL_FX_CHOICES': (
        ('', 'Slide'),
        ('carousel-fade', 'Fade'),
    ),

    'FRONTEND_COL_SIZE_DEFAULT': '',
    'FRONTEND_COL_SIZE_CHOICES': (
        ('', 'Automatically size'),
        ('12', 'Full row'),
        ('6', 'Half - 1/2 column'),
        ('4', 'Thirds - 1/3 column'),
        ('8', 'Thirds - 2/3 column'),
        ('3', 'Quarters - 1/4 column'),
        ('9', 'Quarters - 3/4 column'),
        ('2', 'Sixths - 1/6 column'),
        ('10', 'Sixths - 5/6 column'),
        ('1', 'Twelfths - 1/12 column'),
        ('5', 'Twelfths - 5/12 column'),
        ('7', 'Twelfths - 7/12 column'),
        ('11', 'Twelfths - 11/12 column'),
    ),

    'FRONTEND_COL_BREAK_DEFAULT': 'md',
    'FRONTEND_COL_BREAK_CHOICES': (
        ('', 'Always expanded'),
        ('sm', 'sm - Expand on small screens (phone, 576px) and larger'),
        ('md', 'md - Expand on medium screens (tablet, 768px) and larger'),
        ('lg', 'lg - Expand on large screens (laptop, 992px) and larger'),
        ('xl', 'xl - Expand on extra large screens (wide monitor, 1200px)'),
    ),

    'FRONTEND_NAVBAR_FORMAT_DEFAULT': '',
    'FRONTEND_NAVBAR_FORMAT_CHOICES': (
        ('', 'Default Bootstrap Navbar'),
        ('codered-navbar-center', 'Centered logo at top'),
    ),

    'FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT': 'navbar-light',
    'FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES': (
        ('navbar-light', 'Light - for use with a light-colored navbar'),
        ('navbar-dark', 'Dark - for use with a dark-colored navbar'),
    ),

    'FRONTEND_NAVBAR_CLASS_DEFAULT': 'bg-light',

    'FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT': 'navbar-expand-lg',
    'FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES': (
        ('', 'Never show menu - Always collapse menu behind a button'),
        ('navbar-expand-sm', 'sm - Show on small screens (phone size) and larger'),
        ('navbar-expand-md', 'md - Show on medium screens (tablet size) and larger'),
        ('navbar-expand-lg', 'lg - Show on large screens (laptop size) and larger'),
        ('navbar-expand-xl', 'xl - Show on extra large screens (desktop, wide monitor)'),
    ),

    'FRONTEND_THEME_HELP': "Change the color palette of your site with a Bootstrap theme. Powered by Bootswatch https://bootswatch.com/.",  # noqa
    'FRONTEND_THEME_DEFAULT': '',
    'FRONTEND_THEME_CHOICES': (
        ('', 'Default - Classic Bootstrap'),
        ('cerulean', 'Cerulean - A calm blue sky'),
        ('cosmo', 'Cosmo - An ode to Metro'),
        ('cyborg', 'Cyborg - Jet black and electric blue'),
        ('darkly', 'Darkly - Flatly in night mode'),
        ('flatly', 'Flatly - Flat and modern'),
        ('journal', 'Journal - Crisp like a new sheet of paper'),
        ('litera', 'Litera - The medium is the message'),
        ('lumen', 'Lumen - Light and shadow'),
        ('lux', 'Lux - A touch of class'),
        ('materia', 'Materia - Material is the metaphor'),
        ('minty', 'Minty - A fresh feel'),
        ('pulse', 'Pulse - A trace of purple'),
        ('sandstone', 'Sandstone - A touch of warmth'),
        ('simplex', 'Simplex - Mini and minimalist'),
        ('sketchy', 'Sketchy - A hand-drawn look for mockups and mirth'),
        ('slate', 'Slate - Shades of gunmetal gray'),
        ('solar', 'Solar - A dark spin on Solarized'),
        ('spacelab', 'Spacelab - Silvery and sleek'),
        ('superhero', 'Superhero - The brave and the blue'),
        ('united', 'United - Ubuntu orange and unique font'),
        ('yeti', 'Yeti - A friendly foundation'),
    ),

    'FRONTEND_TEMPLATES_BLOCKS': {
        'cardblock': (
            ('coderedcms/blocks/card_block.html', 'Card'),
            ('coderedcms/blocks/card_head.html', 'Card with header'),
            ('coderedcms/blocks/card_foot.html', 'Card with footer'),
            ('coderedcms/blocks/card_head_foot.html', 'Card with header and footer'),
            ('coderedcms/blocks/card_blurb.html', 'Blurb - rounded image and no border'),
            ('coderedcms/blocks/card_img.html', 'Cover image - use image as background'),
        ),
        'cardgridblock': (
            ('coderedcms/blocks/cardgrid_group.html', 'Card group - attached cards of equal size'),
            ('coderedcms/blocks/cardgrid_deck.html', 'Card deck - separate cards of equal size'),
            ('coderedcms/blocks/cardgrid_columns.html', 'Card masonry - fluid brick pattern'),
        ),
        'pagelistblock': (
            ('coderedcms/blocks/pagelist_block.html', 'General, simple list'),
            ('coderedcms/blocks/pagelist_list_group.html', 'General, list group navigation panel'),
            ('coderedcms/blocks/pagelist_article_media.html', 'Article, media format'),
            ('coderedcms/blocks/pagelist_article_card_group.html',
                'Article, card group - attached cards of equal size'),
            ('coderedcms/blocks/pagelist_article_card_deck.html',
             'Article, card deck - separate cards of equal size'),
            ('coderedcms/blocks/pagelist_article_card_columns.html',
             'Article, card masonry - fluid brick pattern'),
        ),
        'pagepreviewblock': (
            ('coderedcms/blocks/pagepreview_card.html', 'Card'),
            ('coderedcms/blocks/pagepreview_form.html', 'Form inputs'),
        ),
        # templates that are available for all block types
        '*': (
            ('', 'Default'),
        ),
    },

    'FRONTEND_TEMPLATES_PAGES': {
        # templates that are available for all page types
        '*': (
            ('', 'Default'),
            ('coderedcms/pages/web_page.html', 'Web page showing title and cover image'),
            ('coderedcms/pages/web_page_notitle.html', 'Web page without title and cover image'),
            ('coderedcms/pages/home_page.html', 'Home page without title and cover image'),
            ('coderedcms/pages/base.html', 'Blank page - no navbar or footer'),
        ),
    },

    'BANNER': None,
    'BANNER_BACKGROUND': '#f00',
    'BANNER_TEXT_COLOR': '#fff',
}


@lru_cache()
def get_config():
    config = DEFAULTS.copy()
    for var in config:
        cr_var = 'CODERED_%s' % var
        if hasattr(settings, cr_var):
            config[var] = getattr(settings, cr_var)
    return config


cr_settings = get_config()

try:
    import bootstrap4.bootstrap as bootstrap
except ImportError:
    import bootstrap3.bootstrap as bootstrap

get_bootstrap_setting = bootstrap.get_bootstrap_setting
