# setup.py
from setuptools import setup, find_packages

setup(
    name="maxclientapi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["requests", "websocket-client"],  # зависимости, если есть
    author="arsrus721",
    description="Моя первая библиотека Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arsrus721/maxclientapi",  # если есть репозиторий
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
