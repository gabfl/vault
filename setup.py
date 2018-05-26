from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='pyvault',
    version='1.9',
    description='Python password manager',
    long_description=long_description,
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/vault',
    license='MIT',
    packages=['vault', 'vault.lib'],
    package_dir={'vault': 'src'},
    install_requires=['pycryptodome==3.4.11', 'pyperclip', 'tabulate',
                      'argparse', 'passwordgenerator'],  # external dependencies
    entry_points={
        'console_scripts': [
            'vault = vault.vault:main',
        ],
    },
    classifiers=[  # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        #  'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        #  'Development Status :: 5 - Production/Stable',
    ],
)
