from setuptools import setup, find_packages
import sys

install_data = False

if "--install-data" in sys.argv:
    install_data = True
    del sys.argv[sys.argv.index("--install-data")]

setup(
    name="cherab-adas",
    version="1.1.0",
    license="EUPL 1.1",
    namespace_packages=['cherab'],
    packages=find_packages(),
    include_package_data=True
)

# add some ADAS data to local atomic repository
if install_data:
    try:
        from cherab.adas import install_zeeman_structures
        install_zeeman_structures()
    except ImportError:
        pass
