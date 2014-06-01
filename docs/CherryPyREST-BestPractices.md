#Creating a CherryPy REST Server

##Abstract
This document describes the parts and components that can be used to create a
REST server using CherryPy as the base.

Other components that would normally be needed:
    * A Database
    * An ORM for the database
    * A system level configuration system
    * A system level logging configuration

##Configuration
CherryPy provides a flexible configuration system and splits configuration up
into two main parts:
    * **Server level config** - this includes the config for the main server, bus,
	  logging, etc., components that is not specifically involved with serving the
	  current request. It also allows some level of user config to be set up on
	  this level.
	* **Application level config** - this is the configuration specific to the
	  application being served and is centered around the specific config to use
	  for the given URI, any tools attached for the URI and request, etc.

In practice, the CherryPy global config system may be used to fully configure
the system, but since the other components making up the system also needs to be
configured and tested independently, a higher level application config system
will be used.

This is done with a set of functions in the `lib.__init__.py` file. This file
will also export a `conf` value which is the global application configuration
dictionary.

It will also export `appDir` which is the full path to the main app directory.

**Features**:
   * Uses `cherrypy._cpconfig.merge` to build config dictionaries from _INI_
	 style config files.
   * Allows for default config files as well as site local versions to override
	 defaults. For eg: `app.conf` is default and then `app.site.conf` will
	 automatically be the site local config.
   * Set of functions to independently read and generate config dictionaries for
	 system components which automatically takes site local configs into account
	 and can be set that configs may be required or not.
   * `lib.appDir` - full path to the app dir
   * `lib.conf` - main application config from `/etc/app.[site.]conf`
   * CherryPy app configs (request handling configs) are placed in the config
	 dir, then parsed to a dictinary with `lib.componentConfig()` which is then
	 used as the app config when mounting the app to the CP tree.

##Logging
All components uses the CherryPy `logging` system. This makes it easy to
configure all logging functionality from one config file for all components,
instead doing this individually for each component.

**Features**:
    * Uses timed rotating log files to auto rotate at midnight
	* Log dir defaults to `{appDir}/var/log/{appName}/` and will be auto created
	  if it does not exist by `lib.configApp()`
	* Main application log file, `app.log` used for application logging on any
	  level.
	* Log format for `app.log` is such that it will log the name logger to make
	  it easy to track the source of the error. For this to work every module
	  should set up local logger using the module name. The **peewee** ORM
	  already does this.
	* CherryPy access and error logs are separate log files and uses the
	  standard CP log format, but is still set up from the one log config file.

##Tests
??

