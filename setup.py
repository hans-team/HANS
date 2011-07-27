#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, platform
from distutils.core import setup, Command
from DistUtilsExtra.command import *
import glob

# Get current Python version
python_version = platform.python_version_tuple()

# Setup the default install prefix
prefix = sys.prefix
oldvalue=None
# Check our python is version 2.6 or higher
if python_version[0] >= 2 and python_version[1] >= 6:
    ## Set file location prefix accordingly
    prefix = '/usr/local'

# Get the install prefix if one is specified from the command line
for arg in sys.argv:
    if arg.startswith('--prefix='):
        prefix = arg[9:]
        prefix = os.path.expandvars(prefix)

def update_data_path(prefix, oldvalue=None):
    try:
        fin = file('hans/hansconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__hans_data_directory__':
                # update to prefix, store oldvalue
                if not oldvalue:
                    oldvalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefix)
                else: # restore oldvalue
                    line = "%s = %s" % (fields[0], oldvalue)
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find hans/hansconfig.py")
        sys.exit(1)
    return oldvalue

oldvalue=update_data_path(prefix + '/share/hans/')


#class Clean(Command):
#    description = "custom clean command that forcefully removes dist/build directories and update data directory"
#    user_options = []
#    def initialize_options(self):
#        self.cwd = None
#    def finalize_options(self):
#        self.cwd = os.getcwd()
#    def run(self):
#        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
#        os.system('rm -rf ./build ./dist')
#        update_data_path(prefix, oldvalue)



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

        scripts = ['bin/hans'],
        
        data_files = [
            ('bin', ['bin/hans-launcher']),
            ('share/hans/db', glob.glob('data/db/*interface')),
            ('share/hans/db/actions', glob.glob('data/db/actions/*action')),
            ('share/hans/media', glob.glob('data/media/*')),
            ('share/hans/ui', glob.glob('data/ui/*')),
            ('/etc/udev/rules.d', ['udev-rules/99-hans-usb.rules']),
        ],
        cmdclass = { 
                 
            "build" : build_extra.build_extra,
            "build_i18n" :  build_i18n.build_i18n,
            "clean": clean_i18n.clean_i18n,#Clean],
            
        }
)
