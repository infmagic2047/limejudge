import os
import re
from setuptools import Extension, find_packages, setup


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    content = read_file('limejudge/__init__.py')
    regex = r'^__version__ = [\'"]([^\'"]*)[\'"]$'
    match = re.search(regex, content, re.M)
    if not match:
        raise RuntimeError('Cannot find version string in __init__.py')
    return match.group(1)


setup(
    name='limejudge',
    version=get_version(),
    description='Simple judge tool for OI contests',
    long_description=read_file('README.rst'),
    url='https://github.com/infmagic2047/limejudge',
    author='Yutao Yuan',
    author_email='infmagic2047reg@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Education',
    ],
    packages=find_packages(exclude=['tests*']),
    ext_modules=[
        Extension('limejudge.ptrace', ['limejudge/ptrace.c']),
    ],
    install_requires=[
        'PyYAML',
        'docopt',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'limejudge = limejudge.cmdline:main',
        ],
    },
    zip_safe=True,
)
