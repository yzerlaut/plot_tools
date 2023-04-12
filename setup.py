from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='plot_tools',
    version='1.0',
    description='A layer on top of `matplotlib` to achieve flexible & high-standard data visualization across different mediums',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yzerlaut/plot_tools',
    author='Yann Zerlaut',
    author_email='yann.zerlaut@gmail.com',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    keywords='data visualization matplotlib',
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.4",
        "svgutils==0.3.4",
        "numpy>=1.21",
        "scipy>=1.6",
        "scikit-image>=0.16"
    ]
)
