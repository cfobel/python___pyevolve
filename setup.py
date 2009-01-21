# $Id: setup.py 163 2009-01-21 15:13:40Z christian.perone $
from setuptools import setup, find_packages
from pyevolve import __version__, __author__

setup(
   name = "Pyevolve",
   version = __version__,
   packages = find_packages(),
   scripts = ['pyevolve_graph.py'],
   package_data = {
      'pyevolve': ['*.txt']
   },
   author = __author__,
   author_email = "christian.perone@gmail.com",
   description = "A complete python genetic algorithm framework",
   license = "PSF",
   keywords = "genetic algorithm algorithms framework library python",
   url = "http://code.google.com/p/pyevolve/", 
   download_url = "http://code.google.com/p/pyevolve/downloads/list"
)
