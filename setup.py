from setuptools import setup

setup(
    name='multipjson',
    version='1.0.0',
    py_modules=['generate_json'],
    entry_points={
        'console_scripts': [
            'multipjson=generate_json:generate_json_objects',
        ],
    },
    install_requires=[
        'requests'
    ],
    author='k4tedu',
    description='Multiple JSON Generator CLI tool',
    python_requires='>=3.6',
)

