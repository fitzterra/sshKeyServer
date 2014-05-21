# -*- coding: utf-8 -*-
"""
Base model definitions for the real models to inherit from.
"""

from external import peewee

# Set up a defered SQLite database to be configured from the data
# L{lib.database.setup} function later
database = peewee.SqliteDatabase(None)

class ModelBase(peewee.Model):
    """
    The base class for all models.

    This class only provides the Meta class for the database connection to be
    used by all models.
    """
    class Meta:
        database = database

