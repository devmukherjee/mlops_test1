# This is an empty file for module: setup.py
import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.0.1"

REPO_NAME = "mlops_test1"
AUTHOR_USER_NAME = "devmukherjee"
AUTHOR_NAME = "Dev Mukherjee"
SRC_REPO = "chicken_disease_classification"
AUTHOR_EMAIL = "devmukherjeeindia@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for chicken disease classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
        }
    ,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"))