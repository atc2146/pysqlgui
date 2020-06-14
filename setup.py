import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysqlgui", # Replace with your own username
    version="1.0.1",
    author="Alex Chung",
    description="A lightweight and intuitive package to interface with SQL in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atc2146/pysqlgui",
    packages=setuptools.find_packages(),
    install_requires=[
          'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	test_suite='nose.collector',
	tests_require=['nose'],
    python_requires='>=3.6',
)