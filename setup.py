from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup (
    name = 'pyvault',
    version = '1.3b',
    description = 'Python password manager',
    long_description = long_description,
    author = 'Gabriel Bordeaux',
    author_email = 'pypi@gab.lc',
    url = 'https://github.com/gabfl/vault',
    license = 'MIT',
    packages = ['vault', 'vault.lib'],
    install_requires = ['pycryptodome', 'pyperclip', 'tabulate', 'argparse'], # external dependencies
    entry_points = {
        'console_scripts': [
            'vault = vault.vault:main',
        ],
    },
)