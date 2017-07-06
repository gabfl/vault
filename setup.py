from setuptools import setup

setup (
    name = 'pyvault',
    version = '1.3',
    description = 'Python password manager',
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
