from setuptools import setup, find_packages

setup(
    name="multipjson",
    version="1.0.0",
    author="k4tedu",
    description="Multiple JSON Generator CLI Tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'multipjson=multipjson.__main__:main',  # <== inilah kuncinya
        ],
    },
    install_requires=[
        "requests",
        "colorama"
    ]
)
