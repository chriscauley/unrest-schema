from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
  name = 'unrest_schema',
  packages = find_packages(),
  version = '0.1.1',
  description = 'Convert Django forms into json schema',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Chris Cauley',
  author_email = 'chris@lablackey.com',
  url = 'https://github.com/chriscauley/unrest-schema',
  keywords = ['utils','django'],
  install_requires = ['django'],
  license = 'MIT',
  include_package_data = True,
)
