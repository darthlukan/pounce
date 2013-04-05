from setuptools import setup

setup(
    name='Pounce',
    version='1.0',
    author='Brian Tomlinson',
    author_email='darthlukan@gmail.com',
    url='https://github.com/darthlukan/pounce.git',
    download_url='https://github.com/darthlukan/pounce.git',
    packages=['pounce', 'test'],
    scripts = ['scripts/pounce'],
    install_requires=['progressbar>=2.3',
                      'notify2'],
    license='GPLv2',
    long_description=open('README').read(),
)