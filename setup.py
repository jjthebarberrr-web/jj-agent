"""Setup script for jj-agent."""

from setuptools import setup, find_packages
from pathlib import Path
import os

readme = Path(__file__).parent / "README.md"
readme_content = readme.read_text(encoding="utf-8") if readme.exists() else ""

# Read version from environment or default
version = os.getenv("JJ_VERSION", "0.1.0")

setup(
    name="jj-agent",
    version=version,
    description="Local-first super-agent for code generation and project management",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author="JJ Agent",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "openai>=1.3.0",
        "pyyaml>=6.0.1",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jj=cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "capabilities.yaml",
            "capabilities.prod.yaml",
            "*.service",
            "logrotate.conf",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
