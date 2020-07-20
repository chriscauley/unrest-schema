from setuptools import setup, find_packages

setup(
  name = 'unrest_schema',
  packages = find_packages(),
  version = '0.1',
  description = '',
  long_description="",
  long_description_content_type="text/markdown",
  author = 'Chris Cauley',
  author_email = 'chris@lablackey.com',
  url = 'https://github.com/chriscauley/unrest-schema',
  keywords = ['utils','django'],
  install_requires = ['django'],
  license = 'MIT',
  include_package_data = True,
)
