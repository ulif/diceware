import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests_path = os.path.join(os.path.dirname(__file__), 'tests')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        args = sys.argv[sys.argv.index('test')+1:]
        self.test_args = args
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

tests_require = [
    'pytest >= 2.0.3',
    'pytest-xdist',
    'pytest-cov',
    ]

docs_require = [
    'Sphinx',
    ]

setup(
    name="diceware",
    version="0.1",
    author="Uli Fouquet",
    author_email="uli@gnufix.de",
    description=(
        "Passphrases you will remember."),
    license="GPL 3.0",
    keywords="diceware password passphrase",
    url="https://github.com/ulif/diceware/",
    py_modules=['diceware', ],
    packages=[],
    namespace_packages=[],
    long_description=read('README.rst') + '\n\n\n' + read('CHANGES.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'diceware = diceware:main',
        ]
        }
)
