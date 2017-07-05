from setuptools import setup

setup (
    name = 'Vault',
    version = '1.3',
    description = 'Python password manager',
    author = 'Gabriel Bordeaux',
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
