# -*- coding: utf-8 -*-

import os.path
import sys

from setuptools import setup, find_packages


def recursive(*dirpaths):
    offset = len(os.path.join('interview', ''))
    dirs = [os.path.join('interview', d) for d in dirpaths]
    return ['{}/*'.format(d)[offset:] for d in dirs] + [
        os.path.join(path, directory, '*')[offset:]
        for dirpath in dirs
        for path, directories, filenames in os.walk(dirpath)
        for directory in directories
    ]


sys_path = sys.path[:]
sys.path[:] = (os.path.abspath('interview'),)
__import__('__meta__')
sys.path[:] = sys_path

meta = sys.modules['__meta__']
meta_app = meta.__app__
meta_version = meta.__version__
meta_description = meta.__description__

# requirements = ''

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    requirements = [
        req for req in requirements
        if req != ''
        and req.strip()[0] != '#'
        and '--' not in req
    ]


setup(
    name=meta_app,
    author="",
    author_email="",
    version=meta_version,
    description=meta_description,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords=['interview'],
    packages=find_packages(
        include=['interview', 'interview.*'],
        exclude=('tests',)
    ),
    package_data={  # ignored by sdist (see MANIFEST.in), used by bdist_wheel
        'interview': recursive(
		'files',
		'schemas'
	),
    },
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    zip_safe=False,
    platforms='any',
    entry_points = {
         'console_scripts': ['interview=interview.__main__:main'],
    }

)
