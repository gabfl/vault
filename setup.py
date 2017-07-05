from setuptools import setup

setup(
   name = 'Vault',
   version = '1.3',
   description = 'Python password manager',
   author = 'Gabriel Bordeaux',
   install_requires = ['pycryptodome', 'pyperclip', 'tabulate', 'argparse'], # external dependencies
)
