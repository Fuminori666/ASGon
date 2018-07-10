from setuptools import setup, find_packages

setup(
    name="ASGon",
    version="0.1",
    author="Anton Chebanov",
    author_email="anton.chebanov01@gmail.com",
    description=("Project for ASGon airsoft club "),
    packages=find_packages(),
    install_requires=['Flask', 'flask_wtf', 'flask_sqlalchemy', 'flask_migrate']
)
