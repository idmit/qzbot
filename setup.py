# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='qzbot',
    version='0.1.0',
    description='Telegram Quiz Bot',
    long_description=readme,
    author='Ivan Dmitrievsky',
    author_email='ivan.dmitrievsky+python@gmail.com',
    url='https://github.com/idmit/qzbot',
    install_requires=[
        "python-telegram-bot",
    ],
    license=license_,
    packages=find_packages(exclude=('tests', 'docs')))
