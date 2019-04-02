'''Setup for making overall package
'''
__author__ = "Ag Stephens"
__date__ = "31 Mar 2019"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Ag.Stephens@stfc.ac.uk"
from setuptools import setup, find_packages

# One strategy for storing the overall version is to put it in the top-level
# package's __init__ but Nb. __init__.py files are not needed to declare 
# packages in Python 3
from land_ingest import __version__ as _package_version

# Populate long description setting with content of README
#
# Use markdown format read me file as GitHub will render it automatically
# on package page
with open("README.md") as readme_file:
    _long_description = readme_file.read()
    
    
setup(
    name='glamod-land-ingest',
    version=_package_version,
    description='Ingestion library and utilities for ingesting land observations',
    author=__author__,
    author_email=__contact__,
    url='https://github.com/glamod/glamod-land-ingest',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See LICENSE file for details',
    packages=find_packages(),
    package_data={},
    install_requires=['requests'],
    
    # This qualifier can be used to selectively exclude Python versions - 
    # in this case early Python 2 and 3 releases
    python_requires='>=3.5.0', 
    
    # See:
    # https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [ ],
        }
)
