#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from glob import glob
from os.path import join as pjoin


from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE
)

from setuptools import setup


# The name of the project
name = 'desdeo_vis'

# Ensure a valid python version
ensure_python('>=3.3')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    name: [
        'nbextension/static/*.*js*',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/desdeo_vis',
        nb_path, '*.js*'),
    ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'desdeo_vis.json')
]


cmdclass = create_cmdclass(
    'jsdeps',
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)

cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:all'),
    #ensure_targets(jstargets),
)


setup_args = dict(
    name='desdeo-vis',
    description=(
        'Visualisations and preference selection widgets for the '
        + 'DESDEO interactive multiobjective optimization library'),
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_packages(),
    author='Frankie Robertson',
    author_email='frankie@robertson.name',
    url='https://github.com/industrial-optimization-group/desdeo-vis',
    license='MPL 2.0',
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Framework :: Jupyter',
    ],
    include_package_data=True,
    install_requires=[
        'ipywidgets>=7.0.0',
        'widgetsnbextension',
        'desdeo>=0.1.3',
        'matplotlib',
        'altair',
        'vega',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'nbval',
        ],
        'docs': [
            'sphinx',
            'recommonmark',
            'sphinx_rtd_theme',
            'nbsphinx>=0.2.13',
            'jupyter_sphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
            "sphinx_autodoc_typehints",
        ],
        "dev": ["black==18.4a4", "twine", "flake8", "isort"],
    },
    entry_points={},
    package_data={
        'desdeo_notebooks': [
            '*.ipynb',
            'output/*.ipynb',
        ]
    }
)

if __name__ == '__main__':
    setup(**setup_args)
