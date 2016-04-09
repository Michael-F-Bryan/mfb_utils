from setuptools import find_packages, setup


setup(
    name='utils',
    version='0.1',
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
    license='MIT',
    long_description=open('README.rst').read(),
    author='Michael F Bryan',
    description='My utility scripts',
)
