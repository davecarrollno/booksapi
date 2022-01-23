from codecs import open
from os import path
import os
import sys
import shutil
import platform
import sysconfig
from setuptools import setup,setuptools,find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.install_scripts import install_scripts
from distutils import log
from glob import glob

pkg = sysconfig.get_paths()["platlib"] + '/booksapi'

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):

        ver = sys.version_info[:2]
        if ver == (3, 10):
            version = '3.10'

        install.run(self)


with open("README.txt", "r") as fh:
    long_description = fh.read()

    setup(
        name="booksapi",
        version="2022.1.23.1",
        author="Dave Carroll",
        author_email="dcarroll@example.com",
        description="Simple API for containerized book search",
        keywords = ['api'],
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="git location",
        packages = find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
        ],
        python_requires='>=3.9',
        install_requires=[ "alembic==1.7.5",
                           "click==8.0.3",
                           "Flask==2.0.2",
                           "Flask-HTTPAuth>=4.2.0",
                           "Flask-Migrate==3.1.0",
                           "Flask-SQLAlchemy==2.5.1",
                           "Flask-HTTPAuth==4.2.0",
                           "flask-marshmallow==0.14.0",
                           "marshmallow==3.14.1",
                           "marshmallow-sqlalchemy==0.27.0",
                           "greenlet==1.1.2",
                           "Jinja2==3.0.3",
                           "MarkupSafe==2.0.1",
                           "itsdangerous==2.0.1",
                           "Mako==1.1.6",
                           "psycopg2==2.9.3",
                           "python-dotenv==0.19.2",
                           "SQLAlchemy==1.4.31",
                           "urllib3==1.26.8",
                           "Werkzeug>=1.0.1"
        ],
        include_package_data=True,
        scripts =[
                  ],
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
    )