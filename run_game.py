#!/usr/bin/env python
"""Point of execution for play.

Configures module path and libraries and then calls lib.main.main.

"""

import getopt
import os
import sys
import textwrap
import traceback


def prepare_path():
    """Load the source directory in to sys.path.

    This is only necessary when running a source distribution. Binary
    distributions ensure that the module path contains the modules anyway.

    """
    if os.path.exists("lib"):
        sys.path.insert(1, "lib")


def fix_avbin_loader():
    """Monkey patch pyglet.lib to load AVBin from the current directory on
    OS X if it is found.

    WARNING: this is currently required to make sure that the py2app
    distribution launches correctly on systems without AVBin.

    """
    from pyglet.lib import loader
    find_library = loader.find_library
    def fixed_find_library(name):
        if loader.platform == "darwin" and os.path.exists("libavbin.dylib") \
                and name == "avbin":
            return "libavbin.dylib"
        return find_library(name)
    loader.find_library = fixed_find_library


def set_debug(debug):
    """Set the debug flag in the constants module to the given value.

    :Parameters:
        `debug` : bool
            The value to set.

    """
    try:
        import constants
        constants.DEBUG = debug
    except ImportError, exc:
        print "error: could not find source directory"
        sys.exit(1)


def parse_args():
    """Parse command line arguments.

    For details of what the options do see USAGE_MESSAGE (defined below).

    """
    import config as config
    from constants import DEBUG, VERSION

    ## Construct the usage message.
    USAGE_MESSAGE = textwrap.dedent("""\
    usage: %s [OPTIONS]...
    Mandatory arguments for long options are required for short options too.

      -h, --help                    print this usage message
      -v, --version                 print version information
    """ % os.path.basename(os.path.join(".", sys.argv[0])))

    ## Add debug options to usage message.
    if DEBUG: USAGE_MESSAGE += textwrap.dedent("""\

    Debug options
    -------------
      -p, --profile                 run in the profiler
    """)

    ## Utility functions
    def usage(exit_code):
        print USAGE_MESSAGE
        sys.exit(exit_code)
    def version():
        print u"v%s" % VERSION
        sys.exit()
    def assert_debug():
        if not DEBUG:
            usage(2)

    ## Parse arguments.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvp", ["help", "version",
                                   "profile"])
    except getopt.GetoptError, exc:
        usage(2)

    ## No additional arguments.
    if len(args) > 0:
        usage(2)

    ## Process options.
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        elif opt in ("-v", "--version"):
            version()
        elif opt in ("-p", "--profile"):
            assert_debug()
            config.profile = True
        else:
            usage(2)


def run(debug=False):
    """Run the game.

    Prepares the top level before launching the game. The aim is to make moving
    from development to production simple, and to ensure differences between
    distributions are ironed out before starting the game.

    :Parameters:
        `debug` : bool
            The value to set for constants.DEBUG.

    """
    prepare_path()
    fix_avbin_loader()
    set_debug(debug)
    parse_args()

    try:
        import main
        main.main()
    except Exception, exc:
        open("error.log", "w").write(traceback.format_exc())
        raise


if __name__ == "__main__":

    # Change to the game directory
    os.chdir(os.path.dirname(os.path.join(".", sys.argv[0])))

    # Start the actual game
    run()
