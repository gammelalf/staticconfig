import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="staticconfig",
    version="0.0.6",
    author="Wolfgang Fischer",
    author_email="31348226+gammelalf@users.noreply.github.com",
    description="Json config files with a statically defined structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gammelalf/staticconfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
