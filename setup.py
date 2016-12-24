import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup_requires = [
    'pytest_runner',
    ]

install_requires = [
    'setuptools',
    ]

tests_require = [
    # See tox.ini
    'pytest >=2.8.3',
    'coverage',
    ]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    ]

setup(
    name="diceware",
    version="0.9.1",
    author="Uli Fouquet",
    author_email="uli@gnufix.de",
    description=(
        "Passphrases you will remember."),
    license="GPL 3.0",
    keywords="diceware password passphrase",
    url="https://github.com/ulif/diceware/",
    py_modules=[],
    packages=['diceware', ],
    namespace_packages=[],
    long_description=read('README.rst') + '\n\n\n' + read('CHANGES.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security :: Cryptography",
        (
            "License :: OSI Approved :: "
            "GNU General Public License v3 or later (GPLv3+)"),
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    entry_points={
        'console_scripts': [
            'diceware = diceware:main',
        ],
        'diceware_random_sources': [
            'system = diceware.random_sources:SystemRandomSource',
            'realdice = diceware.random_sources:RealDiceRandomSource',
            # add more sources of randomness here...
        ],
    },
)
