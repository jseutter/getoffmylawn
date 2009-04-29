"""Configuration parameters stored in a module namespace.

This file is loaded during the program initialisation before the main module is
imported. Consequently, this file must not import any other modules, or those
modules will be initialised before the main module, which means that command
line options may not have been registered.

Parameters come in two types, those that are stored in the config file and those
that aren't. Running the profiler is an example of the former; fullscreen mode
would be an example of the latter.

Just because an option is stored in the config file doesn't mean it can't also
be changed by, for example, a command line switch. But doing so should not
alter the config file's value.

The `save_option` method is used to alter a value here and in the config file.
It can only be called for a predefined list of options. The `save_all` method
should probably not be used. It will write all current values for config file
parameters to the config file.

"""

# IMPORTANT!
# Never do "from config import ...". This module relies on manipulation of its
# own namespace to work properly.
__all__ = []


class LocalConfig(object):
    """Manager for the local config file.

    """

    def __init__(self, **defaults):
        """Create a LocalConfig object.

        Keyword arguments define the import local config options and their
        default values.

        """
        import constants
        self.defaults = defaults
        self.locals = dict(defaults)
        self.config_file = constants.CONFIG_FILE
        self.load()

    def load(self):
        """Read the config file.

        """
        config_scope = {}
        open(self.config_file, "a").close()
        exec open(self.config_file) in config_scope
        for name in self.defaults:
            value = config_scope.get(name, self.defaults[name])
            self.locals[name] = globals()[name] = value

    def save(self):
        """Write the config file.

        """
        config_fd = open(self.config_file, "w")
        for key in self.defaults:
            value = self.locals[key]
            if value != self.defaults[key]:
                line = "%s = %r\n" % (key, value)
                config_fd.write(line)
        config_fd.close()

    def save_option(self, name, value=None):
        """Change an option in the config file.

        :Parameters:
            `name` : str
                The name of the option to save.
            `value` : object
                The value to set.

        """
        assert name in self.defaults
        if value is not None:
            globals()[name] = value
        self.locals[name] = globals()[name]
        self.save()

    def save_all(self):
        """Save all current values to the config file.

        """
        for name in self.defaults:
            self.locals[name] = globals()[name]
        self.save()


# Default values for non-persistent options.
profile = False

# Default values for persistent options.
local = LocalConfig(
    fullscreen = False,
    width = 800,
    height = 600
)

# See the module docstring for details of these methods.
save_option = local.save_option
save_all = local.save_all

# Clean up the module namespace.
del local, LocalConfig
