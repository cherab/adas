from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import sys
import numpy
import os
import os.path as path
import multiprocessing

threads = multiprocessing.cpu_count()
force = False
profile = False
install_rates = False

if "--force" in sys.argv:
    force = True
    del sys.argv[sys.argv.index("--force")]

if "--profile" in sys.argv:
    profile = True
    del sys.argv[sys.argv.index("--profile")]

if "--install-rates" in sys.argv:
    install_rates = True
    del sys.argv[sys.argv.index("--install-rates")]

compilation_includes = [".", numpy.get_include()]

setup_path = path.dirname(path.abspath(__file__))

# build extension list
extensions = []
for root, dirs, files in os.walk(setup_path):
    for file in files:
        if path.splitext(file)[1] == ".pyx":
            pyx_file = path.relpath(path.join(root, file), setup_path)
            module = path.splitext(pyx_file)[0].replace("/", ".")
            extensions.append(Extension(module, [pyx_file], include_dirs=compilation_includes),)

cython_directives = {
    'language_level': 3
}
if profile:
    cython_directives['profile'] = True


setup(
    name="cherab-adas",
    version="1.1.0",
    license="EUPL 1.1",
    namespace_packages=['cherab'],
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(extensions, nthreads=threads, force=force, compiler_directives=cython_directives)
)

# setup a rate repository with common rates
if install_rates:
    try:
        from cherab.adas import repository
        repository.populate()
    except ImportError:
        pass
