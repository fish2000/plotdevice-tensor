from __future__ import print_function

from pprint import pformat
from os import getcwd, walk, system
from os.path import splitext, join, relpath, isdir
from distutils.core import Command
from distutils.dir_util import remove_tree
from setuptools import setup
from setuptools.extension import Extension

CLASSIFIERS = (
    "Development Status :: 3 - Alpha",
    "Environment :: MacOS X :: Cocoa",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python",
    "Topic :: Artistic Software",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
    "Topic :: Multimedia :: Video",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: User Interfaces",
    "Topic :: Text Editors :: Integrated Development Environments (IDE)")

frameworks = join(getcwd(), 'Frameworks')
gpuimage_libs = join(frameworks,  'GPUImage.framework', 'Versions', 'A')
gpuimage_headers = join(gpuimage_libs, 'Headers')

def find_filters(base_path=join('tensorlib', "filters")):
    filters = dict()
    for root_path, dirs, files in walk(base_path):
        for file_name in files:
            if file_name.lower().endswith('filter.m'):
                filter_name, _ = splitext(file_name)
                filters[filter_name] = join(root_path, filter_name)
    return filters

def get_sources(filter_dict, suffix="m"):
    return ["%s.%s" % (filter_pth, suffix) for filter_pth in filter_dict.values()]

def write_filter_header(filter_dict):
    headers = get_sources(filter_dict, suffix="h")
    with open(join("tensorlib", "filters.h"), 'wb') as header_fh:
        header_fh.write('''#import "filters/FilterBase.h"\n\n''')
        header_fh.writelines(
            ['''#import "%s"\n''' % relpath(header, start='tensorlib') for header in headers])

class CleanCommand(Command):
    description = "wipe out ./build and ./dist dirs"
    user_options = []
    trees = ('./build', './dist', './tensorlib/build', './plotdevice_tensorlib.egg-info')
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        system('find . -iname .ds_store -print -delete')
        system('find . -name \*.pyc -print -delete')
        for tree in self.trees:
            if isdir(tree):
                remove_tree(tree)
        system('rm -rf MANIFEST.in PKG')

filters = find_filters()
source_files = ['module.m', 'filters/FilterBase.m']
sources = [join('tensorlib', tensorlib_file) for tensorlib_file in source_files]
sources.extend(get_sources(filters))
write_filter_header(filters)

tensorlib = Extension('tensorlib',
    sources=sources,
    extra_compile_args=[
        '-Wno-error=unused-command-line-argument-hard-error-in-future',
        '-Wno-unused-function',
        '-Qunused-arguments',
        '-DTENSORLIB_STDOUT',
        '-DTENSORLIB_STDERR',
        '-F%s' % frameworks],
    extra_link_args=[
        '-Wno-error=unused-command-line-argument-hard-error-in-future',
        '-L%s' % gpuimage_libs,
        '-F%s' % frameworks,
        '-framework', 'AppKit',
        '-framework', 'Foundation',
        '-framework', 'GPUImage'])

if __name__ == '__main__':
    import sys
    from clint.textui import puts, colored
    build_commands = [
        'build', 'build_ext', 'build_clib',
        'install', 'install_lib']
    if set(sys.argv).intersection(set(build_commands)):
        puts(colored.yellow('Building tensorlib with %d filters:' % len(filters)))
        puts(colored.cyan(pformat(sorted(filters.keys()), indent=4)))

setup(name="plotdevice-tensorlib",
    version="0.1.0",
    author="Alexander Bohn",
    author_email="fish2000@gmail.com",
    url="http://github.com/fish2000/plotdevice-tensorlib",
    description="GPU-based image processing",
    setup_requires=['clint'],
    cmdclass=dict(
        clean=CleanCommand),
    ext_modules=[tensorlib],
    include_dirs=[gpuimage_headers],
    classifiers=CLASSIFIERS)
