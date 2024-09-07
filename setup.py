from setuptools import setup, find_packages

setup(
    name="pyChain",
    version="0.1.0",
    author="mr-wuliu",
    author_email="mr_wuliu@foxmail.com",
    description="A package for creating chainable method calls in Python",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    platforms=["any"],
)

