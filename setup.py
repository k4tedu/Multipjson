from setuptools import setup, find_packages

setup(
    name="multipjson",
    version="1.0.0",
    description="Multiple JSON Generator CLI Tool",
    author="k4tedu",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'multipjson = multipjson.generate_json:main',
        ],
    },
    install_requires=[
        "requests",
        "colorama"
    ],
)
