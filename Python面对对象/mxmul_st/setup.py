import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="mxmul_pkg",
    version='0.1.0',
    author='zhangxin',
    author_email='879086359@qq.com',
    description='An exaple for teaching how to publish a Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'http://',
    packages = setuptools.find_packages(),
    classifiers=["Programming Language::Python ::3",
                 "Licence ::OSI Approved ::MIT License",
                 "Operating System ::OS Indepent",],
)

