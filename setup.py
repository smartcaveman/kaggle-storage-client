import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaggle-storage-client",
    version="0.0.1",
    author="smartcaveman",
    author_email="smartcaveman@gmail.com",
    description="Provides a simplified interface for using kaggle datasets as a remote data file storage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smartcaveman/kaggle-storage-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: File Sharing"
    ],
    python_requires=">=3.7",
    install_requires=["kaggle"]
)