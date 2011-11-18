from distutils.core import setup

setup(
        name='Piddle',
        version='0.1-dev',
        author='Brian Tomlinson',
        author_email='darthlukan@gmail.com',
        url='https://bitbucket.org/darthlukan/piddle',
        packages=['piddle', 'test',],
        license='GPLv2',
        long_description=open('README').read(),
)
