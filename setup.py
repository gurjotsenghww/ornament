from setuptools import setup, find_packages

setup(
    name="ornament",
    version="0.1.0",
    description="Ornàment: Autonomous AI Website Engineer",
    author="Ornàment Team",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ornament=ornament.cli.main:main",
        ],
    },
    python_requires=">=3.10",
)
