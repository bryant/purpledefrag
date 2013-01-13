from setuptools import setup


packages = ["bunny", "purpledefrag", "purpledefrag.q3df", "testsuite"]

dependencies = [
    # todo: figure out dependencies
    "lxml"
]

setup(
    name = "purpledefrag",
    version = "0.1",
    packages = packages,
    install_requires = dependencies
)
