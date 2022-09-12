from setuptools import setup

pkgname = "pydevkit"
modname = pkgname.replace('-', '_')

setup(
    name=pkgname,
    # use_scm_version=True,
    use_scm_version={'write_to': 'src/__version__.py'},
    setup_requires=["setuptools_scm"],
    description="python development kit",
    long_description=open("README-short.md", "r").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
    ],
    url="https://github.com/aanatoly/pydevkit",
    author="Anatoly Asviyan",
    author_email="aanatoly@gmail.com",
    license="GPLv2",
    packages=[
        modname,
        modname + '.log'
    ],
    package_dir={
        modname: 'src',
        modname + '.log': 'src/log'
    },
    install_requires=[
    ],
    extras_require={
        "dev": ["tox", "twine"]
    },
    zip_safe=False,
)
