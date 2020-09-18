
from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

with open(os.path.join(root_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

for dirpath, dirnames, filenames in os.walk('dieterpy'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)

setup(
    name='dieterpy',
    version="0.1.0",
    packages=packages,
    author="Carlos Gaete-Morales",
    author_email="cdgaete@gmail.com",
    install_requires=['exceltogdx',
                      'pandas == 1.0.5',
                      'pyyaml == 5.3.1',
                      'psutil',
                      'matplotlib',
                      'plotly',
                      'streamlit'],
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "dieterpy = dieterpy.__main__:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/x-rst",
    description='DIETERpy GAMS-Python framework of a power system model DIETER',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ],
)
