# setup.py
from setuptools import setup, find_packages

setup(
    name="maxclientapi",
    version="2.3.0",
    packages=find_packages(),
    install_requires=["websocket-client"], 
    author="arsrus721",
    description="A Python library for working with the 'MAX Messenger' WebSocket API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arsrus721/maxclientapi", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)


