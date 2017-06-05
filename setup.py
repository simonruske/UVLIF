from setuptools import setup

setup(name="UVLIF2", 
      version='0.1', 
      description='Package for reading and analysing UVLIF data',
      author='Simon Ruske',
      license='MIT',
      packages=['UVLIF2'], 
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
)
