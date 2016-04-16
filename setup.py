import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests_path = os.path.join(os.path.dirname(__file__), 'tests')


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test"), ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)                                # pragma: no cover


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    'setuptools',
    'gnupg >=2.0.2',
    ]

tests_require = [
    # See tox.ini
    'pytest >=2.8.3',
    'coverage',
    'six >=1.10.0',
    ]

docs_require = [
    'Sphinx',
    ]

setup(
    name="diceware",
    version="0.6.2.dev0",
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
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    cmdclass={'test': PyTest},
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
