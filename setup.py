import os
from setuptools import setup
from coderedcms import __version__

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8"
) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="coderedcms",
    version=__version__,
    packages=["coderedcms"],
    include_package_data=True,
    license="BSD License",
    description="Wagtail-based CMS by CodeRed for building marketing websites.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/coderedcorp/coderedcms",
    author="CodeRed LLC",
    author_email="info@coderedcorp.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.8,<4.12",  # should be the same as wagtail
        "django-eventtools==1.0.*",
        "django-bootstrap5==23.3",
        "Django>=4.1,<5.1",  # should be the same as wagtail
        "geocoder==1.38.*",
        "icalendar==5.0.*",
        "wagtail>=5.0,<6.0",
        "wagtail-cache>=2.3,<3",
        "wagtail-seo>=2.4,<3",
    ],
    entry_points={
        "console_scripts": ["coderedcms=coderedcms.bin.coderedcms:main"]
    },
    zip_safe=False,
)
