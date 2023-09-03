from setuptools import setup

setup(
    packages=["cli", "lib"],
    package_dir={
        "": ".",
        "cli": "./cli",
        "lib": "./lib",
    },
)
