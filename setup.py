## -*- encoding: utf-8 -*-
"""
Semantic annotations for the SageMath library
"""

import os
import sys
# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.test import test as TestCommand
# To use a consistent encoding
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("/opt/sage-git2/sage -t --force-lib sage_annotations")
        sys.exit(errno)

setup(
    name='sage-semantic-annotations',
    version='0.1.0',
    description='Semantic annotations for the SageMath library',
    long_description=long_description,
    url='https://github.com/nthiery/sage-semantic-annotations',
    author='Nicolas M. Thiéry',
    author_email='nthiery@users.sf.net',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research'
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
    keywords='SageMath',
    packages=['sage_annotations'],
    install_requires=['recursive-monkey-patch'], # 'Sage'
    cmdclass = {'test': SageTest},
)
