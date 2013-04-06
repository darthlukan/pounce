from setuptools import setup

setup(
    name='Pounce',
    version='1.1',
    author='Brian Tomlinson',
    author_email='darthlukan@gmail.com',
    maintainer='Brian Tomlinson',
    maintainer_email='darthlukan@gmail.com',
    url='https://github.com/darthlukan/pounce.git',
    download_url='https://github.com/darthlukan/pounce.git',
    packages=['pounce', 'test'],
    scripts = ['scripts/pounce'],
    install_requires=['distribute',
                      'progressbar>=2.3',
                      'notify2'],
    license='GPLv2',
    description='A simple CLI file downloader written for Python-3.x',
    long_description=open('README').read(),
)