from setuptools import setup, find_packages

setup(
    name="excel_merger",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "tqdm",
    ],
    entry_points={
        'console_scripts': [
            'excelmerge = src.main:main',
        ],
    },
    author="Dylan Picart",
    author_email="dpicart@partnershipwithchildren.org",
    description="A Python tool to automate merging Excel sheets with dynamic column mapping",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/dylanpicart/excel_merger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
