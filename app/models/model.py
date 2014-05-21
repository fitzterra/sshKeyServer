# -*- coding: utf-8 -*-
"""
Defines the models for the app.
"""

from _BaseModel import database, ModelBase
from external.peewee import *

# NOTE: All models that need to be automatically managed by
# L{lib.database.initialize} should be added to this list.
__all__ = ["database",
           # Models
           "Domain", "Host", "User", "AuthorizedKeys"]

class Domain(ModelBase):
    """
    The Domain table.
    """

    #: Domain name
    name = TextField(unique=True)

    #: Any optional user comments for this domain
    comment = TextField(null=True, default=None)

class Host(ModelBase):
    """
    The hosts within L{Domain}s table.
    """

    #: The L{Domain} FK for this host
    domain = ForeignKeyField(Domain, related_name='hosts', on_delete='CASCADE')

    #: The name for the host
    name = TextField(null=False)

    #: Any optional user comments for this host
    comment = TextField(null=True, default=None)

    def fqn(self):
        """
        Returns the fully qualified name for the host and domain.
        """
        return "{0}.{1}".format(self.name, self.domain.name)

class User(ModelBase):
    """
    The users with accounts on L{Host}s.
    """

    #: The L{Host} FK fpr this user account
    host = ForeignKeyField(Host, related_name='users', on_delete='CASCADE')
    
    #: The name for the user
    name = TextField(null=False)

    #: The SSH public key for this user
    pubKey = TextField(null=False)

    #: Any optional comments for this user
    comment = TextField(null=True, default=None)

    def fqn(self):
        """
        Returns the fully qualified user@host.domain.
        """
        return "{0}@{1}".format(self.name, self.host.fqn())

class AuthorizedKeys(ModelBase):
    """
    Representation of ~/.ssh/authorized_keys file for a L{User}.
    """

    #: The owner of the authorized_keys file
    owner = ForeignKeyField(User, related_name='authorized_keys',
                            on_delete='CASCADE')

    #: The authorized user
    authedUser = ForeignKeyField(User, related_name='accessTo',
                            on_delete='CASCADE')

    #: Any optional SSH options for the authorized entry in the file
    options = TextField(null=True, default=None)

