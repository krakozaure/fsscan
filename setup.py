import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fsscan",
    version="0.0.3",
    author="krakozaure",
    author_email="",
    description="Directory scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krakozaure/fsscan",
    packages=setuptools.find_packages(),
    install_requires=[
        'scandir;python_version<"3.5"'
    ],
    tests_require=[
        "pytest"
    ],
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "Topic :: System :: Filesystems",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ),
    entry_points={
        "console_scripts": [
            "fsscan=fsscan.__main__:main"
        ],
    },
)
