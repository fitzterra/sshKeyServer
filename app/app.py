#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Main sshKeyServer application.
"""

from lib import conf, configFiles, logger, database as db
import cherrypy

def parseArgs():
    """
    Parses command line args.
    """
    logger.debug("In parseArgs...")

def setup():
    """
    Sets the application up
    """
    logger.debug("In setup...")

    # Set up the database
    db.setup()

    # First configure the main CP server with default, and optional site local
    # configs
    for cfg in configFiles('server', required=True):
        cherrypy.config.update(cfg)

    # Add the API app
    import api
    # Set it up
    app = api.setup()

def initialize():
    """
    Initializes the system before startup.
    """
    logger.debug("In initialize...")

def run():
    """
    Run the main system
    """
    logger.debug("In run....")
    logger.debug("Full config %s", conf)

    # Start the server
    cherrypy.engine.start()
    cherrypy.engine.block()

def main():
    """
    Main system startup.
    """
    logger.debug("In main...")

    # Command line args...
    parseArgs()

    # Set up...
    setup()

    # Init...
    initialize()

    # Run...
    run()

if __name__ == "__main__":
    main()
