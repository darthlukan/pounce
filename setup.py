from distutils.core import setup

setup(
    name='Piddle',
    version='0.2.dev',
    author='Brian Tomlinson',
    author_email='darthlukan@gmail.com',
    url='https://github.com/darthlukan/piddle.git',
    download_url='https://github.com/darthlukan/piddle.git',
    packages=['piddle', 'test'],
    install_requires=['python>=2.7.2',
                      'progressbar>=2.3',
                      'urllib3',
                      'notify2'],
    license='GPLv2',
    long_description=open('README').read(),
)