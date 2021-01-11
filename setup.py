import os
from setuptools import setup
from coderedcms import __version__

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='coderedcms',
    version=__version__,
    packages=['coderedcms'],
    include_package_data=True,
    license='BSD License',
    description='Wagtail-based CMS by CodeRed for building marketing websites.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/coderedcorp/coderedcms',
    author='CodeRed LLC',
    author_email='info@coderedcorp.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4>=4.8,<4.9',     # should be the same as wagtail
        'django-eventtools==1.0.*',
        'django-bootstrap4>=2.0,<2.4',
        'Django>=2.2,<3.2',             # should be the same as wagtail
        'geocoder==1.38.*',
        'icalendar==4.0.*',
        'wagtail==2.11.*',
        'wagtailfontawesome>=1.2.*',
        'wagtail-cache==1.*',
        'wagtail-import-export>=0.2,<0.3'
    ],
    entry_points={
        "console_scripts": [
            "coderedcms=coderedcms.bin.coderedcms:main"
        ]
    },
    zip_safe=False,
)
