# -*- coding: utf-8 -*-
# ##################################
#   ____                     _     #
#  / ___|___  _ __ ___   ___| |_   #
# | |   / _ \| '_ ` _ \ / _ \ __|  #
# | |__| (_) | | | | | |  __/ |_   #
#  \____\___/|_| |_| |_|\___|\__|  #
#                                  #
#        Copyright (c) 2023        #
#      rd2md Development Team      #
#       All rights reserved        #
####################################

import io
import os

import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(file, name="__version__"):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


__version__ = get_version(os.path.join(HERE, "rd2md/_version.py"))

with io.open(os.path.join(HERE, "README.md"), encoding="utf8") as fh:
    long_description = fh.read()

setup_args = dict(
    name="rd2md",
    version=__version__,
    url="https://github.com/comet-ml/rd2md",
    author="rd2md development team",
    description="Converter from R docs to markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "rd2md",
    ],
    entry_points={"console_scripts": ["rd2md = rd2md.__main__:main"]},
    python_requires=">=3.6",
    license="MIT License",
    platforms="Linux, Mac OS X, Windows",
    keywords=["python", "r"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
