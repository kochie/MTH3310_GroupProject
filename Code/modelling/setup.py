from setuptools import setup

setup(name='',
      version='0.1',
      description='A set of tools for modelling systems',
      url='http://github.com/kochie/pymodelling',
      author='Robert Koch',
      author_email='robert@kochie.io',
      license='MIT',
      packages=['funniest'],
      install_requires=[
        'numpy',
        'matplotlib'
      ],
      zip_safe=False)