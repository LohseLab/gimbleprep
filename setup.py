from setuptools import setup, find_packages

setup(
    packages=["cli", "lib"],
    package_dir={
        "": ".",
        "cli": "./cli",
        "lib": "./lib",
    },
)