# -*- coding: utf-8 -*-
"""
Key management library.
"""

import re
from lib import database as db

#: Regex to split 'user@host.domain.tld' string into it's components
uhdSplitter = re.compile('^([^@]+)@([^.]+)\.(.*)$')

def splitUserHostDomain(uhd):
    """
    Splits a 'user@host.domian' string into it's 3 components and returns them
    as a tuple of ('user', 'host', 'domain.part').

    @param uhd: the 'user@host.domain' string to split.

    @return: A tuple of ('user', 'host', 'domain.part') if L{uhd} is valid, or
        None otherwise.
    """
    r = uhdSplitter.search(uhd.strip())

    return r.groups() if r else None


def addUserAndKey(uhd, pubKey, allowUpdate=False):
    """
    Adds a new user and public key to the system, or updates the public key for
    an existing if L{allowUpdate) is True.

    This function will not allow duplicate hosts per domain, or duplicate users
    per host.domain to be created. It will only create the domain if this domain
    does not already exists, then only create the host if host in this domain
    domain does not already exist, and only then create the user if the user in
    this host.domain does not exist.

    If the uer@host.domain does exists, and allowUpdate is C{True}, then this
    user's key will be updated by L{pubKey}. If allowUpdate is C{False}, a
    ValueError will be raised indicate that the user exists but no updates are
    allowed.

    @param uhd: The 'user@host.domain.tld' identifier for this user
    @param pubKey: This user's public key
    @param allowUpdate: Allows/disallows updating the key for an existing user.

    @return: The L{db.User} object just added on success.

    @raises: Possibly various errors depending on reason for error.
    """

    # First split the uhd string
    res = splitUserHostDomain(uhd)
    if res is None:
        raise ValueError("Invalid uhd identifier: {0}".format(uhd))

    # Break the parts out
    u, h, d = res

    # Try to create the domain
    try:
        dom = db.Domain.create(name=d)
    except db.IntegrityError:
        # It exists
        dom = db.Domain.select().where(db.Domain.name==d).get()
    
    # Now the host
    try:
        host = dom.addHost(h)
    except db.IntegrityError:
        # It exists
        host = db.Host.select()\
                .where(db.Host.domain==dom)\
                .where(db.Host.name==h)\
                .get()
    
    # Now the user
    try:
        user = host.addUser(u, pubKey)
    except db.IntegrityError:
        # It exists. Unless updates are allowed, we need to bail here
        if not allowUpdate:
            raise ValueError("Key updates to existing user [{0}] not "
                             "allowed.".format(uhd))
        # We may update the key, so get the user
        user = db.User.select()\
                .where(db.User.host==host)\
                .where(db.User.name==u)\
                .get()
        # Update the key
        user.pubKey = pubKey
        user.save()
    
    return user

