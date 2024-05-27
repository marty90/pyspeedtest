from setuptools import setup

setup(
    name='pyspeedtest',
    version='1.0',
    packages=['pyspeedtest'],
    url='https://github.com/marty90/pyspeedtest',
    license='GPL-3.0 license',
    author='Martino Trevisan',
    author_email='martino.trevisan@polito.it',
    description='Simple package that uses Selenium to automate tests from speedtest.net',
    install_requires=['selenium']
)
