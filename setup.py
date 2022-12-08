from setuptools import setup

requirements = [
    'beautifulsoup4==4.7.1',
    'bs4==0.0.1',
    'certifi==2022.12.7',
    'chardet==3.0.4',
    'idna==2.8',
    'json2html==1.2.1',
    'nose==1.3.7',
    'python-dateutil==2.7.5',
    'requests==2.21.0',
    'six==1.12.0',
    'soupsieve==1.7.1',
    'tabulate==0.8.2',
    'urllib3==1.24.1'
]

setup(name='stackstats',
      version='0.1',
      description='StackStatsAPI',
      url='',
      author='Panagiotis Kapsalis',
      author_email='kapsali29@gmail.com',
      license='MIT',
      keywords='StackExchange API',
      packages=['stackstats'],
      install_requires=requirements,
      entry_points={
          'console_scripts': ['stats=stackstats.command_line:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
