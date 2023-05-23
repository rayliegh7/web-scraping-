from setuptools import find_packages,setup
from typing import List

def get_requirement(file_name:str)->List[str]:
    requirement=[]
    with open (file_name) as file_obj:
        requirements=file_obj.readlines()
        requirement=[req.replace("\n"," ") for req in requirements]
        if '-e .' in requirement:
            requirement.remove('-e .')
    return requirement


    

setup(
    name="web scraping",
    author="suryakant ghodke",
    version="0.0.1",
    author_email="suryakantghodake20@gmail.com",
    packages=find_packages(),
    install_requires=get_requirement('requirement.txt') 
)