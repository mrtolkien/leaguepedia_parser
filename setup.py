import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="leaguepedia_parser",
    version="1.0a11",
    packages=[
        "leaguepedia_parser",
        "leaguepedia_parser/parsers",
        "leaguepedia_parser/transmuters",
        "leaguepedia_parser/site",
    ],
    url="https://github.com/mrtolkien/leaguepedia_parser",
    license="MIT",
    author='Gary "Tolki" Mialaret',
    install_requires=["mwclient", "lol_dto >= 0.1a4", "lol_id_tools >= 1.4.0"],
    author_email="gary.mialaret+pypi@gmail.com",
    description="A parser for Leaguepedia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
