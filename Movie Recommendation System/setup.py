from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "Movie-Recommendation-System-Using-Machine-Learning"
AUTHOR_USER_NAME = "Abhishek Choudhary"
SRC_REPO = "movie_recommender"
LIST_OF_REQUIREMENTS = ['streamlit']


setup(
    name=SRC_REPO,                                                          # Name of the package
    version="0.0.1",                                                        # Initial version of my package
    author=AUTHOR_USER_NAME,                                                # Author's name
    description="A small package for Movie Recommendation System",          # Short description of the package
    long_description=long_description,                                      # Long description read from README file
    long_description_content_type="text/markdown",                          # Type of the long description
    url=f"https://github.com/Abhishekjat004/Machine-Learning-Projects",     # URL of the repository
    author_email="abhishekchoudhary533246@gmail.com",                       # Author's email
    packages=[SRC_REPO],                                                    # List of packages to be included
    license="MIT",                                                          # License type
    python_requires=">=3.12",                                                # Minimum Python version required
    install_requires=LIST_OF_REQUIREMENTS                                   # List of dependencies required for the package
)