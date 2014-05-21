System Requirements
===================

## Config setup

### Requirements
* Config using CP config system, but also be available without CP
* Maybe a base config that get's merged into the CP config on CP startup?
* The base config still applies when using iPython for example to test the ORM,
  db and libs...
* Site local configs to apply over default configs:
* Split config in these sections/files:
    * `system.conf`
        * global system configuration
        * parsed with ConfigParser
        * Defines system wide config not specific to any single component
        * Made available to all via: 'from lib import conf'
    * `server.conf`
        * All CP server component config options
        * Will be parsed with cherrypy.config.update()
    * `app_restAPI.conf`
        * Config for the REST API app on /api
    * `app_web.conf`
        * Config for the web app on /
        * This will include all static configs for static content
* Allow `system.conf` and `system.local.conf` to be overriden by command
  line config options when starting the app

## Logging
* Logging must work when local ORM, db, libs testing as well as when running
  under CP or behind nginx
* Must auto rotate using the TimedRotatingFileHandler
* Must be configured via standard base config settings or the logging.config
  mechanism
* Logging in exception handlers should use the logger.exception() method
* All libs/modules should set up thier own loggers, but set the handler to the
  NullHandler and allow the main app to set the root level handler to the
  TimedRotatingFileHandler handler

### Questions:
  - Let CP log to `access.log` and `error.log`, and have the rest of the
    app log to `app.log`?
  - How to configure CP logging seperate from app logging? Can this be
    combined in one config file?

