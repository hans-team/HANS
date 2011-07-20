#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, platform
from distutils.core import setup
from DistUtilsExtra.command import *
import glob

# Get current Python version
python_version = platform.python_version_tuple()

# Setup the default install prefix
prefix = sys.prefix

# Check our python is version 2.6 or higher
if python_version[0] >= 2 and python_version[1] >= 6:
    ## Set file location prefix accordingly
    prefix = '/usr/local'

# Get the install prefix if one is specified from the command line
for arg in sys.argv:
    if arg.startswith('--prefix='):
        prefix = arg[9:]
        prefix = os.path.expandvars(prefix)

# Gen .in files with @PREFIX@ replaced
#for filename in ['udev-discover']:
#    infile = open(filename + '.in', 'r')
#    data = infile.read().replace('@PREFIX@', prefix)
#    infile.close()
#
#    outfile = open(filename, 'w')
#    outfile.write(data)
#    outfile.close()

setup(
        name='hans',
        version='0.1',
        description='Hardware Actions and Notification System.',
        author='David Amian Valle',
        author_email='damian@emergya.com',
        url='https://launchpad.net/hans',

        classifiers=[
            'Development Status :: 0.1 - Alpha',
            'Environment :: Desktop Environment',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX',
            'Programming Language :: Python',
	        'Topic :: Utilities'
        ],
        
        keywords = ['python', 'udev', 'gnome'],

        packages = ['hans', 'hans.actions', 
            'hans.model'], 
        package_dir =  {'hans': 'hans', 
            'hans.actions': 'hans/actions',
            'hans.model': 'hans/model',
            },

        scripts = ['bin/hans.py'],
        
        data_files = [
            ('bin', ['bin/hans']),
            ('share/hans/db', glob.glob('data/db/*interface')),
            ('share/hans/db/actions', glob.glob('data/db/actions/*action')),
            ('share/hans/media', glob.glob('data/media/*')),
            ('share/hans/ui', glob.glob('data/ui/*')),
            ('/etc/udev/rules.d', ['udev-rules/99-hans-usb.rules']),
        ],
        cmdclass = { 
            "build" : build_extra.build_extra,
            "build_i18n" :  build_i18n.build_i18n,
            "clean": clean_i18n.clean_i18n,
        }
)
