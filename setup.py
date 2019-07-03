import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perkle",
    version="0.0.4",
    author="William Borgeaud",
    author_email="williamborgeaud@gmail.com",
    description="Python 3 implementation of Merkle Trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wborgeaud/perkle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)