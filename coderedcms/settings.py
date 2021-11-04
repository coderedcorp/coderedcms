import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _
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
        ('btn-sm', _('Small')),
        ('', _('Default')),
        ('btn-lg', _('Large')),
    ),

    'FRONTEND_BTN_STYLE_DEFAULT': 'btn-primary',
    'FRONTEND_BTN_STYLE_CHOICES': (
        ('btn-primary', _('Primary')),
        ('btn-secondary', _('Secondary')),
        ('btn-success', _('Success')),
        ('btn-danger', _('Danger')),
        ('btn-warning', _('Warning')),
        ('btn-info', _('Info')),
        ('btn-link', _('Link')),
        ('btn-light', _('Light')),
        ('btn-dark', _('Dark')),
        ('btn-outline-primary', _('Outline Primary')),
        ('btn-outline-secondary', _('Outline Secondary')),
        ('btn-outline-success', _('Outline Success')),
        ('btn-outline-danger', _('Outline Danger')),
        ('btn-outline-warning', _('Outline Warning')),
        ('btn-outline-info', _('Outline Info')),
        ('btn-outline-light', _('Outline Light')),
        ('btn-outline-dark', _('Outline Dark')),
    ),

    'FRONTEND_CAROUSEL_FX_DEFAULT': '',
    'FRONTEND_CAROUSEL_FX_CHOICES': (
        ('', _('Slide')),
        ('carousel-fade', _('Fade')),
    ),

    'FRONTEND_COL_SIZE_DEFAULT': '',
    'FRONTEND_COL_SIZE_CHOICES': (
        ('', _('Automatically size')),
        ('12', _('Full row')),
        ('6', _('Half - 1/2 column')),
        ('4', _('Thirds - 1/3 column')),
        ('8', _('Thirds - 2/3 column')),
        ('3', _('Quarters - 1/4 column')),
        ('9', _('Quarters - 3/4 column')),
        ('2', _('Sixths - 1/6 column')),
        ('10', _('Sixths - 5/6 column')),
        ('1', _('Twelfths - 1/12 column')),
        ('5', _('Twelfths - 5/12 column')),
        ('7', _('Twelfths - 7/12 column')),
        ('11', _('Twelfths - 11/12 column')),
    ),

    'FRONTEND_COL_BREAK_DEFAULT': 'md',
    'FRONTEND_COL_BREAK_CHOICES': (
        ('', _('Always expanded')),
        ('sm', _('sm - Expand on small screens (phone, 576px) and larger')),
        ('md', _('md - Expand on medium screens (tablet, 768px) and larger')),
        ('lg', _('lg - Expand on large screens (laptop, 992px) and larger')),
        ('xl', _('xl - Expand on extra large screens (wide monitor, 1200px)')),
    ),

    'FRONTEND_NAVBAR_FORMAT_DEFAULT': '',
    'FRONTEND_NAVBAR_FORMAT_CHOICES': (
        ('', _('Default Bootstrap Navbar')),
        ('codered-navbar-center', _('Centered logo at top')),
    ),

    'FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT': 'navbar-light',
    'FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES': (
        ('navbar-light', _('Light - for use with a light-colored navbar')),
        ('navbar-dark', _('Dark - for use with a dark-colored navbar')),
    ),

    'FRONTEND_NAVBAR_CLASS_DEFAULT': 'bg-light',

    'FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT': 'navbar-expand-lg',
    'FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES': (
        ('', _('Never show menu - Always collapse menu behind a button')),
        ('navbar-expand-sm', _('sm - Show on small screens (phone size) and larger')),
        ('navbar-expand-md', _('md - Show on medium screens (tablet size) and larger')),
        ('navbar-expand-lg', _('lg - Show on large screens (laptop size) and larger')),
        ('navbar-expand-xl', _('xl - Show on extra large screens (desktop, wide monitor)')),
    ),

    'FRONTEND_THEME_HELP': _("Change the color palette of your site with a Bootstrap theme. Powered by Bootswatch https://bootswatch.com/."),  # noqa
    'FRONTEND_THEME_DEFAULT': '',
    'FRONTEND_THEME_CHOICES': (
        ('', _('Default - Classic Bootstrap')),
        ('cerulean', _('Cerulean - A calm blue sky')),
        ('cosmo', _('Cosmo - An ode to Metro')),
        ('cyborg', _('Cyborg - Jet black and electric blue')),
        ('darkly', _('Darkly - Flatly in night mode')),
        ('flatly', _('Flatly - Flat and modern')),
        ('journal', _('Journal - Crisp like a new sheet of paper')),
        ('litera', _('Litera - The medium is the message')),
        ('lumen', _('Lumen - Light and shadow')),
        ('lux', _('Lux - A touch of class')),
        ('materia', _('Materia - Material is the metaphor')),
        ('minty', _('Minty - A fresh feel')),
        ('pulse', _('Pulse - A trace of purple')),
        ('sandstone', _('Sandstone - A touch of warmth')),
        ('simplex', _('Simplex - Mini and minimalist')),
        ('sketchy', _('Sketchy - A hand-drawn look for mockups and mirth')),
        ('slate', _('Slate - Shades of gunmetal gray')),
        ('solar', _('Solar - A dark spin on Solarized')),
        ('spacelab', _('Spacelab - Silvery and sleek')),
        ('superhero', _('Superhero - The brave and the blue')),
        ('united', _('United - Ubuntu orange and unique font')),
        ('yeti', _('Yeti - A friendly foundation')),
    ),

    'FRONTEND_TEMPLATES_BLOCKS': {
        'cardblock': (
            ('coderedcms/blocks/card_block.html', _('Card')),
            ('coderedcms/blocks/card_head.html', _('Card with header')),
            ('coderedcms/blocks/card_foot.html', _('Card with footer')),
            ('coderedcms/blocks/card_head_foot.html', _('Card with header and footer')),
            ('coderedcms/blocks/card_blurb.html', _('Blurb - rounded image and no border')),
            ('coderedcms/blocks/card_img.html', _('Cover image - use image as background')),
        ),
        'cardgridblock': (
            ('coderedcms/blocks/cardgrid_group.html', _('Card group - attached cards of equal size')),
            ('coderedcms/blocks/cardgrid_deck.html', _('Card deck - separate cards of equal size')),
            ('coderedcms/blocks/cardgrid_columns.html', _('Card masonry - fluid brick pattern')),
        ),
        'pagelistblock': (
            ('coderedcms/blocks/pagelist_block.html', _('General, simple list')),
            ('coderedcms/blocks/pagelist_list_group.html', _('General, list group navigation panel')),
            ('coderedcms/blocks/pagelist_article_media.html', _('Article, media format')),
            ('coderedcms/blocks/pagelist_article_card_group.html',
                _('Article, card group - attached cards of equal size')),
            ('coderedcms/blocks/pagelist_article_card_deck.html',
             _('Article, card deck - separate cards of equal size')),
            ('coderedcms/blocks/pagelist_article_card_columns.html',
             _('Article, card masonry - fluid brick pattern')),
        ),
        'pagepreviewblock': (
            ('coderedcms/blocks/pagepreview_card.html', _('Card')),
            ('coderedcms/blocks/pagepreview_form.html', _('Form inputs')),
        ),
        # templates that are available for all block types
        '*': (
            ('', _('Default')),
        ),
    },

    'FRONTEND_TEMPLATES_PAGES': {
        # templates that are available for all page types
        '*': (
            ('', _('Default')),
            ('coderedcms/pages/web_page.html', _('Web page showing title and cover image')),
            ('coderedcms/pages/web_page_notitle.html', _('Web page without title and cover image')),
            ('coderedcms/pages/home_page.html', _('Home page without title and cover image')),
            ('coderedcms/pages/base.html', _('Blank page - no navbar or footer')),
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
