from setuptools import setup, find_packages

setup(
    name='theoneapi',
    version='0.1.0',    
    description='A Python SDK for The One API',
    url='https://github.com/alex-lindsay/alex-lindsay-api',
    author='Alex Lindsay',
    author_email='alexander.m.lindsay.jr+github@gmail.com',
    license='',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  
        'Operating System :: MacOS',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)