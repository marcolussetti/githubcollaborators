import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="githubcollaborators",
    version="0.0.1",
    author="Marco Lussetti",
    author_email="packages@marcolussetti.com",
    description="List collaborators for all of a user's repositories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcolussetti/githubcollaborators",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=[
        'bin/githubcollaborators'
    ],
    install_requires=[
        'requests'
    ]
)
