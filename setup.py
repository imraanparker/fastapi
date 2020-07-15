import os
import sys

__title__ = "FastAPI Template"
__version__ = "0.0.1"
__author__ = "Imraan Parker"
__authoremail__ = "imraan@techie.com"
__url__ = ""
__license__ = "Apache Software License 2.0"
__copyright__ = "Copyright 2020 Imraan Parker"

if sys.version_info < (3, 8):
    print("%s requires Python 3.8 or later." % __title__)
    sys.exit(1)

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(path, "README.md")).read()
except IOError:
    README = ""

with open(os.path.join("app", "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name=__title__,
    version=__version__,
    description="%s can be used to start a new API project" % __title__,
    long_description=README,
    author=__author__,
    author_email=__authoremail__,
    url=__url__,
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    zip_safe=False,
    license=__license__,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Object Brokering",
    )
)