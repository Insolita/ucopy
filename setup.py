from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ucopy',
    version='1.0.0',
    description='Union copier:copy files from one or more dirs to target and autorename files if same already presents',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['ucopy'],
    author='Insolita',
    author_email='webmaster100500@ya.ru',
    keywords=['copy', 'move', 'rename'],
    url='https://github.com/Insolita/ucopy',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    scripts=['bin/ucopy']
)