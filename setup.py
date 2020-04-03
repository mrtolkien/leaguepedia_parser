import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='leaguepedia_parser',
    version='0.2.1',
    packages=['leaguepedia_parser'],
    url='https://github.com/mrtolkien/leaguepedia_parser',
    license='MIT',
    author='Tolki',
    install_requires=['mwclient'],
    author_email='gary.mialaret+pypi@gmail.com',
    description='A parser for the Leaguepedia website, focused on accessing esports data.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
