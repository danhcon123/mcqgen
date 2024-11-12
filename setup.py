from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='duchai',
    author_email='gauvatich123@gmail.com',
    install_requires=["openai","langchain-community", "streamlit","python-dotenv", "PyPDF2"],
    packages=find_packages()
)