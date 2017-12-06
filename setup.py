from setuptools import setup

setup(name="UVLIF", 
      version='0.1', 
      description='Package for reading and analysing UVLIF data',
      author='Simon Ruske',
      license='GPL-3.0',
      packages=['UVLIF'], 
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
)
