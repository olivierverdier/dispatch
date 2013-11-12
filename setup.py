from distutils.core import setup

setup(
    name = 'dispatcher',
    maintainer = 'Olivier Verdier',
    maintainer_email = 'olivier.verdier@gmail.com',
    description = 'A library for event-driven programming',
    packages = [
        'dispatch',
        'dispatch.tests',
    ],
    version = '1.0',
    url = 'https://github.com/olivierverdier/dispatch',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
