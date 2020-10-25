#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Joseph Malemela",
    author_email='itukzz96@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A gateway API for controlling and monitoring a wireless sensor network Digi-Xbee Modules",
    entry_points={
        'console_scripts': [
            'LowCostSmartFarmHub=LowCostSmartFarmHub.cli:main',
        ],
    },
    install_requires=[
        'digi-xbee',
        'click',
        'rpi_ws281x'
    ],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='LowCostSmartFarmHub',
    name='LowCostSmartFarmHub',
    packages=find_packages(include=['LowCostSmartFarmHub','LowCostSmartFarmHub/','LowCostSmartFarmHub.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/itumeleng96/LowCostSmartFarmHub',
    download_url= 'https://github.com/itumeleng96/LowCostSmartFarmHub/archive/0.1.4.tar.gz',
    version='0.1.4',
)
