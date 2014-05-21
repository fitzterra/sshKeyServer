# -*- coding: utf-8 -*-
"""
Application library module
"""
import os
import cherrypy

#: Will always be the .../app dir
appDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

#: The app config dict. It will be initialized by L{configApp}.
conf = {}

def configApp():
    """
    Sets up the app L{conf}ig dictionary from the C{app.conf} and
    C{app.local.conf} config files in C{etc}.
    """
    # The etc dir should be one dir up from where this __file__ is
    etc = os.path.realpath(os.path.join(appDir, 'etc'))
    # It should exist
    assert os.access(etc, os.R_OK|os.X_OK), \
            "Missing or inaccessible ./etc/ dir: {0}".format(etc)

    # The app.[local].conf file(s)
    for cf in ['app.conf', 'app.local.conf']:
        cfg = os.path.join(etc, cf)
        # This is dumb because it makes both config files optional!
        if os.access(cfg, os.R_OK):
            cherrypy._cpconfig.merge(conf, cfg)

# Always run configApp when importing or using this file
configApp()
