from setuptools import setup

setup(name='dnagui',
      version='0.1',
      description='Set Based Design GUI',
      url='http://github.com/storborg/funniest',
      author='ANCR',
      author_email='ANCR@unknown.com',
      license='TBD',
      packages=['dnagui'],
      intall_require=[
          'matplotlib', 'networkx','pillow','numpy',
      ],
      zip_safe=False)
