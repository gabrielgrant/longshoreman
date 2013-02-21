from setuptools import setup

setup(
    name='longshoreman',
    version='0.1.0',
    author='Gabriel Grant',
    author_email='g@briel.ca',
    url='https://github.com/gabrielgrant/longshoreman',
    packages=['longshoreman'],
    license='LGPL',
    long_description=open('README.md').read(),
    install_requires=[
        'gevent_subprocess',
    ],
)
