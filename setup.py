from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "requirements.txt")) as f:
    requirements = f.readlines()

setup(
    name='hcskr',

    version='1.13.0',

    description='코로나 자가진단 라이브러리 (Automation tool for https://hcs.eduro.go.kr/)',
    license='GPL-V3',
    author='LeoK & covid-hcs',

    # author_email='support@leok.kr',
    url='https://github.com/covid-hcs/hcs-python',

    download_url='https://github.com/covid-hcs/hcs-python',

    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=requirements,

    packages=find_packages(),

    keywords=['korea', 'covid', 'auto', 'hcs'],

    python_requires='>=3',


    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 5 - Production/Stable',
    ],
)
