
1. Organize Your Project Structure

Ensure your framework is structured properly, something like this:

selenium-framework/
│── selenium_framework/
│   ├── __init__.py
│   ├── base.py
│   ├── utils.py
│── tests/
│── setup.py
│── pyproject.toml
│── README.md
│── requirements.txt

The selenium_framework/ folder contains your core framework.

__init__.py ensures it can be imported as a package.


2. Create a setup.py File

This file defines the package metadata and dependencies.

from setuptools import setup, find_packages

setup(
    name="selenium-framework",  # Change this to your package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pytest",  # Add other dependencies
    ],
    author="Your Name",
    description="A custom Selenium framework for automation",
    url="https://your-artifactory-url",  # Change this if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

3. Build the Package

Run the following command to generate the distribution files:

python -m build

This will create a dist/ folder containing .tar.gz and .whl files.

4. Upload to Artifactory

If your Artifactory is configured for PyPI packages, you can upload using twine:

twine upload --repository-url https://your-artifactory-url/artifactory/api/pypi/your-repo/ dist/*

Replace your-artifactory-url and your-repo accordingly.

5. Install the Package from Artifactory

Once uploaded, users can install it using:

pip install --index-url https://your-artifactory-url/artifactory/api/pypi/your-repo/simple/ selenium-framework


---

Additional Notes:

Authentication: If Artifactory requires authentication, configure ~/.pypirc:

[your-repo]
repository = https://your-artifactory-url/artifactory/api/pypi/your-repo/
username = your-username
password = your-password

Then upload using:

twine upload --repository your-repo dist/*

Versioning: Bump the version in setup.py before each new upload.

