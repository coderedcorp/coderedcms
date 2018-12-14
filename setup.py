import os
from setuptools import find_packages, setup
from coderedcms import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='coderedcms',
    version=__version__,
    packages=find_packages(),
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'django-eventtools==0.9.*',
        'django-bootstrap4',
        'django>=1.11,<2.2',
        'geocoder>=1.38.1,<2.0',
        'icalendar==4.0.*',
        'wagtail==2.3.*',
        'wagtailfontawesome>=1.1.3,<2.0',
        'wagtail-cache==0.2.*',
        'wagtail-import-export>=0.1,<0.2'
    ],
    extras_require={
        'dev': [
            'pylint-django',
            'sphinx',
            'twine',
        ]
    },
    entry_points="""
            [console_scripts]
            coderedcms=coderedcms.bin.coderedcms:main
    """,
    zip_safe=False,
)
