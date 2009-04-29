#!/usr/bin/env python
"""Setup script for three varieties of distribution:
  * sdist -- A tarball containing the sources and data.
  * py2exe -- A Win32 package independent of python and libraries.
  * py2app -- An OSX package independent of python and libraries.

"""

import os
#import readline
import shutil
import subprocess
import sys
import tarfile
import zipfile

# Change to the game directory
os.chdir(os.path.dirname(os.path.join(".", sys.argv[0])))

# Put the source directory on the module path.
sys.path.insert(1, "lib")

# Record the version
import constants, test_game
version, modified, switched = test_game.get_version_data()
open("VERSION.txt", "wb").write(constants.VERSION + ":" + version)


## Configuration data
#####################

# Directory in which to produce packages for distribution. No other directories
# or files will be left after running this script.
DIST_DIR = "dist"

# The following text is included in the package metadata, it is separated from
# it for convenience.
LONG_DESCRIPTION = """\
In this game you try to win. We can have a large amount of text here to describe
the game in brief detail.
"""

# The package metadata. This is not actually used except for the values of
# 'name' and 'version', but this is a convenient place to collect information
# as other kinds of setup script do use this information.
META = {
    "name"             : "My Game",
    "version"          : constants.VERSION,
    "license"          : "",
    "url"              : "http://www.example.com/~jsmith/mygame",
    "author"           : "John Smith",
    "author_email"     : "j.smith@example.com",
    "description"      : "A game where you try to win.",
    "long_description" : LONG_DESCRIPTION,
}

# The 'lib' directory should NOT be listed here. If additional packages are
# in the game directory then they should be listed here.
PACKAGES = ["pyglet", "_elementtree"]

# If set, then AVBin will be packaged in the binary distributions. If pyglet is
# in PACKAGES then this option is likely wanted also.
PACKAGE_AVBIN = True

# The following paths will be packaged as resources.
RESOURCES = ["data", "VERSION.txt"]

# The following paths will be packaged as top-level resources.
TOPLEVEL = ["README.txt"]

# Configuration data for the source distribution.
SDIST = {
}

# Configuration data for Windows distribution.
PY2EXE = {
    "binary" : META["name"],  # name (no extension) of the resulting executable
    "icon"   : None,          # the .ico resource to use for the executable
}

# Configuration data for the OS X distribution.
PY2APP = {
    "binary"   : META["name"],  # name (no extension) of the resulting bundle
    "icon"     : None,          # the .icns resource to use for the bundle
}

# Filters for files to ignore. If any of these filters return True the file is
# skipped. Arguments are the root and filename.
FILE_FILTERS = [
    lambda r,fn: fn.rsplit(".", 1)[1] in ("pyc", "pyo"),
    lambda r,fn: fn[0] in "#~.",
    lambda r,fn: fn[-1] in "#~",
    lambda r,fn: fn in ("Thumbs.db", ".DS_Store"),
]

# Filters for directories to ignore. If any of these filters return True the
# directory and evertyhing below it are skipped. Arguments are the root and
# directory name.
DIRECTORY_FILTERS = [
    lambda r,dn: dn in ("CVS", ".svn"),
]


## Utility Functions
####################

def get_input(message, options):
    """Get user input on the command line.

    The message is repeated until the input matches something in the sequence
    of options. The options should just be some iterable of strings.

    """
    while True:
        try:
            input = raw_input(message).lower()
        except EOFError:
            print
            sys.exit(1)
        for opt in options:
            if opt.lower() == input.lower():
                return opt

def clean_file(*paths):
    """Join paths and ensure that the resultant file doesn't exist.

    """
    file_path = os.path.join(*paths)
    if os.path.exists(file_path):
        os.remove(file_path)
    return file_path

def clean_dir(*paths):
    """Join paths and ensure that the resultant directory is empty.

    """
    dir_path = os.path.join(*paths)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    return dir_path

def create_zipfile(filename):
    """Create and return a .zip archive from the given base name. If possible,
    compression will be enabled.

    """
    try:
        return zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    except RuntimeError:
        return zipfile.ZipFile(filename, "w", zipfile.ZIP_STORED)

def recurse_files(root):
    """Iterate over files in a directory, recursing into other directories,
    stripping the root filename from the results.

    """
    for base, dirs, files in os.walk(root):
        for file in files:
            path = os.path.join(base, file)
            assert path.startswith(root)
            yield path[len(root)+1:]

def copy_avbin(root):
    """Locate the AVBin binary and copy it to the given directory.

    """
    from pyglet.lib import loader
    lib_name = "avbin"
    if loader.platform == "darwin":
        lib_name = "libavbin.dylib"
    avbin_path = loader.find_library(lib_name)
    file = os.path.basename(avbin_path)
    target_path = os.path.join(root, file)
    shutil.copyfile(avbin_path, target_path)


## Command line parsing
#######################

USAGE_MESSAGE = """\
usage: setup.py sdist|py2exe|py2app

This is a non-standard setup script handling very specific distribution
setups. There are no options other than which distribution you want.
"""

def usage(exit_code):
    print USAGE_MESSAGE
    sys.exit(exit_code)

if len(sys.argv) == 1:
    sys.exit(0)

elif not META["name"]:
    print "setup.py: error: must define META['name'] to build packages"
    sys.exit(1)

elif len(sys.argv) == 2:
    if modified:
        message = "Working copy has local modifications. Continue? [y/n] "
        if get_input(message, "yn") == "n":
            print "Aborted."
            sys.exit(1)
    command = sys.argv[1]

else:
    usage(2)


## Assemble data and sources
############################

class ResourceTree(object):
    """Resource tracker. Paths should be added with the add_path method and
    subpaths will be brought in automatically. Filters are used to determine
    what to keep and what to ignore. Paths are always brought in to the root
    of the tree.

    """

    def __init__(self, *paths):
        """Create a ResourceTree object.

        """
        self.dirs = []
        self.files = []
        for path in paths:
            self.add_path(path)

    def __add__(self, other):
        result = ResourceTree()
        result.dirs = self.dirs
        for dir in other.dirs:
            if dir not in result.dirs:
                result.dirs.append(dir)
        result.files = self.files
        for file in other.files:
            if file not in result.files:
                result.files.append(file)
        return result

    def __iter__(self):
        for dir in self.dirs:
            yield dir
        for file in self.files:
            yield file

    def add_path(self, path, relative=None):
        """Add a single path to the tree.

        """
        # Default relative is current path.
        if relative is None:
            relative = os.path.dirname(path)

        # Compute the length to strip from paths
        rel_length = len(relative)
        if len(relative) > 0:
            rel_length += 1

        # For directories...
        if os.path.isdir(path):
            root, dir = os.path.split(path)
            if all(not filter(root, dir) for filter in DIRECTORY_FILTERS):
                assert path.startswith(relative)
                target_path = path[rel_length:]
                self.dirs.append((path, target_path))
                for name in os.listdir(path):
                    self.add_path(os.path.join(path, name), relative)

        # For files...
        elif os.path.isfile(path):
            root, file = os.path.split(path)
            if all(not filter(root, file) for filter in FILE_FILTERS):
                assert path.startswith(relative)
                target_path = path[rel_length:]
                self.files.append((path, target_path))

    def copy_to(self, target):
        """Copy the tree to a given root directory.

        """
        for dir, target_dir in self.dirs:
            target_dir = os.path.join(target, target_dir)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
        for file, target_file in self.files:
            target_file = os.path.join(target, target_file)
            shutil.copyfile(file, target_file)

resources = ResourceTree()
for path in RESOURCES:
    resources.add_path(path)

top_level = ResourceTree()
for path in TOPLEVEL:
    top_level.add_path(path)

sources = ResourceTree("lib")
for name in PACKAGES:
    package = __import__(name, fromlist=())
    path = os.path.dirname(package.__file__)
    sources.add_path(path)


## Process command
##################

# The functions below are highly procedural, messy and complicated; sadly that's
# how it has to be. They are as thoroughly documented as possible.

def do_sdist():
    """Notes on the `sdist` source distribution:

    * Resultant file is a tarball called 'my-game-1.0.tar.gz'.
    * Launching script is 'run_game.py', 'run_game.pyw' is a copy of that.

    """
    from distutils.core import setup

    # Determine package basename (without extension).
    name = META["name"].lower().replace(" ", "-")
    base = "%s-%s-source" % (name, META["version"])

    # Ensure dist directory exists.
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # Path to the archive.
    tgz_path = clean_file(DIST_DIR, "%s.tar.gz" % base)

    # Create the archive and add sources and resources.
    tgz_package = tarfile.open(tgz_path, "w:gz")
    for path, target in sources + resources + top_level:
        tgz_package.add(path, os.path.join(base, target), False)

    # Add main scripts to the archive.
    tgz_package.add("run_game.py", os.path.join(base, "run_game.py"))
    tgz_package.add("run_game.py", os.path.join(base, "run_game.pyw"))

    # Finish writing and close the archive.
    tgz_package.close()

def do_py2exe():
    """Notes on the `py2exe` win32 executable distribution:

    * Resultant file is a .zip archive called 'my-game-1.0-win32.zip'.
    * That file contains 'My Game.exe', the 'data' folder and other files.

    """
    import py2exe
    from distutils.core import setup

    # Determine package basename (without extension).
    name = META["name"].lower().replace(" ", "-")
    base = "%s-%s-win32" % (name, META["version"])

    # Ensure staging directory exists and is clean.
    staging_path = clean_dir(DIST_DIR, base)

    # Copy main script under the binary name.
    script_path = PY2EXE["binary"] + ".py"
    shutil.copy("run_game.py", script_path)

    # Prepare icon resources.
    icons = [(1, PY2EXE["icon"])] if PY2EXE["icon"] else []

    # Configure and call py2exe setup.
    py2exe_options = {
        "dist_dir"     : staging_path,
        "compressed"   : True,
        "bundle_files" : 1}
    setup(options={"py2exe" : py2exe_options},
          windows=[{"script" : script_path, "icon_resources" : icons}],
          zipfile=None)

    # Clean up main script.
    os.remove(script_path)

    # Copy resources to the staging directory.
    (resources + top_level).copy_to(staging_path)

    # Package system AVBin if required.
    if PACKAGE_AVBIN:
        copy_avbin(staging_path)

    # Path to the archive.
    zip_path = clean_file(DIST_DIR, "%s.zip" % base)

    # Create the archive and add the staging directory.
    zip_package = create_zipfile(zip_path)
    for file in recurse_files(staging_path):
        file_path = os.path.join(staging_path, file)
        zip_package.write(file_path, file)

    # Clean up ZIP staging directory.
    shutil.rmtree(staging_path)

    # Clean up py2exe build directory.
    shutil.rmtree("build")

def do_py2app():
    """Notes on the `py2app` OS X app bundle distribution:

    * Resultant file is a .dmg image called 'my-game-1.0-osx.dmg'.
    * The image contains a 'My Game.app' and top level resources only.

    """
    from setuptools import setup

    # Determine package basename (without extension).
    name = META["name"].lower().replace(" ", "-")
    base = "%s-%s-osx" % (name, META["version"])

    # Ensure staging directory exists and is clean.
    staging_path = clean_dir(DIST_DIR, base)

    # Determine resource directory.
    app_path = os.path.join(staging_path, PY2APP["binary"] + ".app")
    data_path = os.path.join(app_path, "Contents", "Resources")

    # Copy main script under the binary name.
    script_path = PY2APP["binary"] + ".py"
    shutil.copy("run_game.py", script_path)

    # Configure and call py2app setup.
    py2app_options = {
        "argv_emulation" : True,
        "iconfile" : PY2APP["icon"],
        "optimize" : 2,
        "dist_dir" : staging_path,
        "packages" : PACKAGES}
    setup(options={"py2app" : py2app_options},
          app=[script_path],
          data_files=[],
          setup_requires=["py2app"])

    # Clean up main script.
    os.remove(script_path)

    # Embed resources in the app bundle.
    resources.copy_to(data_path)

    # Place top-level resources in the staging directory.
    top_level.copy_to(staging_path)

    # Package system AVBin if required.
    if PACKAGE_AVBIN:
        copy_avbin(data_path)

    # Path to the DMG file.
    dmg_path = clean_file(DIST_DIR, "%s.dmg" % base)

    # Create the disk image.
    command = ["hdiutil", "create", dmg_path, "-srcfolder", staging_path,
               "-volname", META["name"], "-fs", "HFS+", "-format", "UDZO"]
    process = subprocess.Popen(command)
    out_data, err_data = process.communicate()
    if process.returncode != 0:
        if os.path.exists(dmg_path):
            os.remove(dmg_path)

    # Clean up DMG staging directory.
    shutil.rmtree(staging_path)

    # Clean up py2app build directory.
    shutil.rmtree("build")


if command == "sdist":
    do_sdist()
elif command == "py2exe":
    do_py2exe()
elif command == "py2app":
    do_py2app()
else:
    usage(2)
