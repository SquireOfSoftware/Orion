import  sys
from distutils.core import setup

if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name="PDO",
      version="1.3.2",
      py_modules=["pdo"],
      author="NeuroKode Labs, LLC",
      author_email="pdo@neurokode.com",
      maintainer="NeuroKode Labs, LLC",
      maintainer_email="pdo@neurokode.com",
      url="http://pdo.neurokode.com",
      license="BSD License",
      description="PDO; Python Database Objects",
      long_description="PDO: Python Database Objects, is a collection of objects for use with Phase or with the Python Programing Language. PDO is designed to be robust and simple at the same time, allowing access to multiple styles of databases, with one set of instructions. This means never having to worry again about your syntax when changing Database Platforms on your next project.",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities',
          'Topic :: Database',
          'Topic :: Database :: Front-Ends',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ]
      )
