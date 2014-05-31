# -*- coding: utf-8 -*-
"""
The API service package.
"""

import textwrap
import cherrypy
import appInfo
from lib import componentConfig, logger, keyManagement
# This is needed here to make the auth tool checkpassword function get access to
# the auth module
from lib import auth

class API(object):
    """
    The API services root controller class.
    """
    # Here we use the MethodDispatcher, so we expose the class
    exposed = True

    def GET(self):
        """
        Nothing here, so give some help.
        """
        msg = """
        {name} - {version}

        This is the {name} main API entry URI.

        """.format(name=appInfo.name, version=appInfo.version)

        return textwrap.dedent(msg)

class Key(object):
    """
    The .../key/{user@host.domain} API
    """

    exposed = True

    def GET(self, uhd, *args, **kwargs):
        """
        Retrieves the key for C{user@host.domain}

        @param uhd: The user@host.domain string for which to retrieve the key.
        """
        return {uhd: "some key"}

    def POST(self, uhd, key=None, *args, **kwargs):
        """
        Creates the key for C{user@host.domain}.

        @param uhd: The user@host.domain string for which to retrieve the key.
        """
        res = keyManagement.addUserAndKey(uhd, key)

        return res._data


def setup():
    """
    Sets up the '/api' services URI.

    Sets up the API services controller class by creating the interfaces
    hierarchy and mounting it as a cherrypy app on the '/api' path.

    Configuration is read from the C{app[.site].conf} config files.
    """

    # Create the API instance
    api = API()
    api.key = Key()

    # Mount as CP app
    cherrypy.tree.mount(api, '/api', componentConfig('api'))

