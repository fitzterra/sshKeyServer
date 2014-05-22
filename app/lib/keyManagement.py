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


def addUserAndKey(uhd, pubKey):
    """
    Adds a new user and public key to the system.

    @param uhd: The 'user@host.domain.tld' identifier for this user
    @param pubKey: This user's public key

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
        dom = db.Domain.select().where(db.Domain.name == d).get()
    
    # Now the host
    try:
        host = dom.addHost(h)
    except db.IntegrityError:
        # It exists
        host = db.Host.select().where(db.Host.name == h).get()
    
    # Now the user
    user = host.addUser(u, pubKey)
    
    return user

