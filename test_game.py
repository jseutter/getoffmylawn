#!/usr/bin/env python
"""Point of execution for development.

Updates 'VERSION.txt' and then calls run_game.run with the debug flag set.

"""

import os
import subprocess
import sys


def get_version_data():
    """Discern information about the current SVN revision.

    Returns a tuple (version, modified, switched). `version` is a string
    representation of the Subversion revision. `modified` is a flag
    indicating whether the working copy is modified. `switched` is a flag
    indicating whether the working copy is switched.

    `version` can take two special values: "unknown" which is a default
    if the process fails (for example if Subversion isn't installed) and
    "exported" which indicates there is no Subversion control data.

    """
    try:
        proc = subprocess.Popen("svnversion", stdout=subprocess.PIPE)
        pout = proc.communicate()[0]
        assert pout.strip() != "exported"
    except:
        return ("unknown", False, False)

    version = pout.strip().split(":")[-1]
    modified = "M" in version
    switched = "S" in version
    version = version.rstrip("MS")
    return version, modified, switched


if __name__ == "__main__":

    # Change to the game directory
    os.chdir(os.path.dirname(os.path.join(".", sys.argv[0])))

    # Record the version
    version, modified, switched = get_version_data()
    open("VERSION.txt", "wb").write("testing:" + version)

    # Start the actual game
    import run_game
    run_game.run(debug=True)
