from setuptools import setup, find_packages

setup(
    name='notopenai',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',  # Ensure you add all necessary dependencies here.
    ],
    description='A Python client for NotOpenAI API',
    author='Your Name',
    author_email='your.email@example.com',
    keywords='API AI',
)
