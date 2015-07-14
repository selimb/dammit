from setuptools import setup, find_packages

version = "0.1.0"
setup(
    author="Selim Belhaouane",
    author_email="selim.belhaouane@gmail.com",
    name='dammit',
    description="A command-line utility to remove locks on file.",
    version=version,
    license="MIT",
    url="https://github.com/beselim/dammit",
    install_requires=[],
    packages=find_packages(),
    entry_points={'console_scripts': "dammit = dammit.__main__:main"},
    scripts=['bin/handle64.exe', 'bin/activatePID.exe'],
    keywords=('dammit windows shell'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Shells',
        'Operating System :: Microsoft :: Windows :: Windows 7',
    ],
)
