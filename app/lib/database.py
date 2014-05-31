# -*- coding: utf-8 -*-
"""
Databse access library
"""

from lib import conf, appDir
from external import peewee
from models import *

def initialize(create=True, drop=False):
    """
    Initializes the database by creating and/or dropping tables.

    @param create: If True (the default), then any tables that do not exist yet
           will be created.
    @param drop: If True (the default is False), then any table that currently
           exists will first be dropped before it is created. Note that if
           L{create} is False, all existing tables will be dropped.
    """
    # We need the list of models in models.model.__all__ to work with
    from models import model
    # A model will be an instance of this base class
    from external.peewee import BaseModel

    # First drop the tables if that is required
    if drop:
        # Run through all entries in model.__all__
        for n in model.__all__:
            # Get the object
            obj = getattr(model, n)
            if isinstance(obj, BaseModel):
                # It's a table, so drop it without errors if it does not exist,
                # and cascade to any other tables
                obj.drop_table(fail_silently=True, cascade=True)

    # Create any tables that does not exist yet if required
    if create:
        # Run through all entries in model.__all__
        for n in model.__all__:
            # Get the object
            obj = getattr(model, n)
            if isinstance(obj, BaseModel):
                # It's a table, so create it without errors if exist already.
                obj.create_table(fail_silently=True)

def setup(create=True):
    """
    Sets up the database connection and creates any new tables if required.

    @param create: If True (the default), the L{initialize} function will be
           called to create any missing tables after connecting to the database.
    """
    # Get database connection params
    dbBackend = conf['database']['backend']
    dbName = conf['database']['name'].format(appDir=appDir)
    # Set up database
    if dbBackend == 'sqlite':
        database = peewee.SqliteDatabase(dbName, check_same_thread=False)
    else:
        raise ValueError("Unsupported database backend: %s" % dbBackend)
    # Replace the proxy database created for model definitions with the real
    # database
    db_proxy.initialize(database)

    if create:
        # Create while making sure not to drop anything.
        initialize(create=True, drop=False)

