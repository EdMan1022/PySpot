import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

packages = setuptools.find_packages()

setuptools.setup(
    name='PySpot',
    version='1.1',
    author="Edward Brennan",
    author_email="EdMan1022@gmail.com",
    description="A Python implementation of the HubSpot API",
    long_description=long_description,
    url="https://github.com/EdMan1022/PySpot.git",
    packages=packages,
    install_requires=["requests"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
