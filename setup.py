from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    with open(os.path.join("rudag_sdk", "__init__.py"), "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"

setup(
    name="rudag-sdk",
    version=get_version(),
    author="Rudag Network",
    author_email="cmoraes199322@gmail.com",
    description="SDK oficial para interactuar con la blockchain de Rudag Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rudag-Network/rudag-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Blockchain",
        "Topic :: Cryptocurrency",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "ecdsa>=0.17.0",
        "base58>=2.1.0",
        "cryptography>=3.4.7",
        "websockets>=10.0",
        "aiohttp>=3.8.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
        "async": [
            "aiohttp>=3.8.0",
            "websockets>=10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rudag-cli=rudag_sdk.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rudag_sdk": ["py.typed"],
    },
)
