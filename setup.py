from setuptools import setup, find_packages

# ------------------------- #
# binance/binance structure #
# ------------------------- #

setup(
    name="binance",
    version='0.1.0',
    packages=find_packages(),
    package_dir={"binance":"binance"},
    install_requires=[
        "pytest",
        "requests",
        "websocket-client",
    ],
)