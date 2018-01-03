#!/usr/bin/env python
#

DESCRIPTION = "Easy barcode generation"
LONG_DESCRIPTION = """\
makebarcode is dedicated to making barcodes for inventory management.

Some of the features that makebarcode offers are

- make a pdf file to print out for certain label models
- make a single barcode pdf file
"""

DISTNAME = 'makebarcode'
MAINTAINER = 'Brian J. Oney'
MAINTAINER_EMAIL = 'brian.j.oney@gmail.com'
URL = 'https://github.com/oneyb/makebarcode'
LICENSE = 'GPLv2'
DOWNLOAD_URL = 'https://github.com/oneyb/makebarcode'
VERSION = '0.1'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup


def check_dependencies():
    install_requires = []
    try:
        import reportlab
    except ImportError:
        install_requires.append('reportlab')

    return install_requires

if __name__ == "__main__":

    install_requires = check_dependencies()
    # install_requires = []

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=install_requires,
          packages=['makebarcode'],
          classifiers=[
              'Intended Audience :: Entrepreneurial/Inventory',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'License :: OSI Approved :: GPLv2 License',
              'Topic :: Multimedia :: Graphics',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'],
    )
