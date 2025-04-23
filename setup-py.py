from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rideco-safety-risk-analysis",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="FAIR risk analysis for RideCo safety features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rideco-safety-risk-analysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "seaborn>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "rideco-risk-analysis=rideco_risk_analysis.cli:main",
        ],
    },
)
