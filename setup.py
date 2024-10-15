from pathlib import Path

from setuptools import find_packages
from setuptools import setup

HERE = Path(Path(__file__).parent).resolve()
PACKAGE_NAME = "mailjet_rest"

# Dynamically calculate the version based on mailjet_rest.VERSION.
version = "latest"

setup(
    name=PACKAGE_NAME,
    author="starenka",
    author_email="starenka0@gmail.com",
    maintainer="Mailjet",
    maintainer_email="api@mailjet.com",
    version="1.3.3",
    download_url="https://github.com/mailjet/mailjet-apiv3-python/releases/" + version,
    url="https://github.com/mailjet/mailjet-apiv3-python",
    description=("Mailjet V3 API wrapper"),
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: Email",
        "Topic :: Utilities",
    ],
    license="MIT",
    keywords=[
        "Mailjet API v3 / v3.1 Python Wrapper",
        "wrapper",
        "email python-wrapper",
        "transactional-emails",
        "mailjet",
        "mailjet-api",
    ],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["requests>=2.32.3"],
    tests_require=["pytest"],
    entry_points={},
    packages=find_packages(),
)
