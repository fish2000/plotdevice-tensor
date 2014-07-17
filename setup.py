from __future__ import print_function

from pprint import pprint
from os import getcwd, walk
from os.path import splitext, join, relpath
from setuptools import setup
from setuptools.extension import Extension

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
    build_commands = [
        'build', 'build_ext', 'build_clib',
        'install', 'install_lib']
    if set(sys.argv).intersection(set(build_commands)):
        print('Building tensorlib with %d filters:' % len(filters))
        pprint(sorted(filters.keys()))

setup(name="tensorlib",
       version="1.0",
       author="fish2k",
       description="GPU-based image processing",
       ext_modules=[tensorlib],
       include_dirs=[gpuimage_headers])