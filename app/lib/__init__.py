# -*- coding: utf-8 -*-
"""
Application library module
"""
import os, errno
import cherrypy
import logging
import appInfo

#: The main application logger
logger = logging.getLogger('main')

#: The full path to the application base dir.
appDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

#: The app config dict. It will be initialized by L{configApp}.
conf = {}

class ConfigError(Exception):
    """
    Config exception class.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def mkdir_p(path):
    """
    Creates a directory path, also creating parent directories that do not
    exist, the same way 'mkdir -p' does.

    This comes from here: http://stackoverflow.com/a/600612/3671582
    """
    # By not first testing if the directory exists before creating it, we avoid
    # a possible race condition whereby it may be created between the test for
    # it and the subsequent creation if the test indicates it does not exist
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def getLogDir():
    """
    Returns the full path to the application log directory.

    @return: Full path to log dir.
    """
    # The log dir at var/log/{appName}/ relative to the directory the main
    # application lives in.
    logPath = 'var/log/{0}'.format(appInfo.name)
    logDir = os.path.realpath(os.path.join(appDir, logPath))
    # Make sure it exists, creating it if it does not
    mkdir_p(logDir)

    return logDir

def getConfigDir():
    """
    Returns the full path to the application config directory.

    @return: Full path to config dir.
    @raises: L{ConfigError} if config dir not found.
    """
    etc = os.path.realpath(os.path.join(appDir, 'etc'))
    # It should exist
    if not os.access(etc, os.R_OK|os.X_OK):
        raise ConfigError("Missing or inaccessible config dir: {0}".format(etc))

    return etc

def configFiles(component, required=True):
    """
    Returns a list of config files for the L{component} to be configured.

    The app allows seperate config files for the various components used to
    build the full system. Any of these components may have their own config
    file in the app config directory.

    The config system further allows default configs and site local configs for
    each component. Site local configs are meant to override component settings
    for giving site installtion, while the default config for a component should
    be sane values that should be good enough to get the component intialized.

    The config file name format is: C{{component}[.site].conf}

    where L{component} is the component name, C{.site} is only present in the
    site local copy of the config file, and C{.conf} is always present to
    indicate a config file.

    @param component: The component name for which to get the config files.
    @param required: If True (the default) an assertion error will be raised if
           the default config file for the component does not exist. 

    @return: A list of full paths to the config files for this component. This
             list will be empty if there are no config files for the component,
             consist of one element if there is only the default config file, or
             have two elements if a site local config is also present. If a site
             local config is prsent, it will always be the 2nd element in the
             list since a site local config is meant to override the default
             config.

    @raises: L{ConfigError} if no default config file is found for a L{required}
             component, or if other config type errors are detected.
    """
    # Get the config dir
    etc = getConfigDir()

    conf = []

    # First the default conf
    cfg = os.path.join(etc, "{0}.conf".format(component))
    # Is it readable?
    if os.access(cfg, os.R_OK):
        # Yes, we add it to config list
        conf.append(cfg)
    elif required:
        # Nope, and it's required so we raise an error
        raise ConfigError("Required config file for component '{0}' not "
                          "found at {1}".format(component, cfg))
    else:
        # The default component config was not found, so we do not even look for
        # a site local config.
        return conf

    # Check for a site local confi
    cfg = os.path.join(etc, "{0}.site.conf".format(component))
    # Is it readable?
    if os.access(cfg, os.R_OK):
        # Yes, we add it to config list
        conf.append(cfg)

    return conf

def componentConfig(component, required=True):
    """
    Finds the config file(s), reads, parses and merges the configs and returns
    one dictionary with the final config.

    A component may have it's default C{{component}.conf} file in the default
    config dir, as well as a site local config file. See L{configFiles} for more
    details.

    @param: component: The component for which to read the config
    @param: required: If True (the default), then at least the default config
            for the component should be available.

    @return: A dictionary consisting of the config options.
    """
    # The component config dict
    compConf = {}

    # Find all configs for the component
    for cfg in configFiles(component, required=required):
        # Use the CP config merger to read the config and merge it into the
        # component config dict.
        cherrypy._cpconfig.merge(compConf, cfg)

    return compConf

def configApp():
    """
    Sets up the app L{conf}ig dictionary from the C{app.conf} and
    C{app.site.conf} config files in C{etc}.
    """
    global conf

    # Set logging up before anything else. Anything that needs logging should
    # import lib very early
    from logging.config import fileConfig
    # Logging config file
    logConf = os.path.join(getConfigDir(), 'logging.conf')
    # We need to add logDir as attribute of the logging module so the file
    # handlers can know the path to the log dir
    logging.logDir = getLogDir()
    fileConfig(logConf, disable_existing_loggers=False)

    # Get component configs into config
    conf = componentConfig('app', required=True)

# Always run configApp when importing or using this file
configApp()
