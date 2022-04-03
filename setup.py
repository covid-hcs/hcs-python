from os import path
from setuptools import setup, find_packages

GITHUB_REPO = "https://github.com/covid-hcs/hcs-python"
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.readlines()

setup(
    name="covid_hcs",
    version="0.0.1",
    description="코로나 자가진단 라이브러리 (Automation tool for https://hcs.eduro.go.kr/)",
    license="MIT",
    license_file="LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 5 - Production/Stable",
    ],
    author="covid-hcs",
    url=GITHUB_REPO,
    project_urls={
        "Discussions": f"{GITHUB_REPO}/discussions",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    keywords=["korea", "covid", "auto", "hcs"],
    python_requires=">=3.7",
)
