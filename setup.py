from setuptools import setup, find_packages

setup(
    name='binance',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "utils @ git+https://github.com/dfrankmv/utils.git"
    ],
)