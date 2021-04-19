import setuptools

setuptools.setup(
    name="water-place",
    version="0.0.1",
    author="Luisahiris Espinal",
    author_email="luisahiris.ea@gmail.com",
    description="water care",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Luisahiris/water-place",
    project_urls={
        "Bug Tracker": "https://github.com/Luisahiris/water-place/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)