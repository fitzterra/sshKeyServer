# -*- coding: utf-8 -*-
"""
Authentication and access control module.
"""

USERS = {'admin': 'admin'}

def validate_password(realm, username, password):
    if username in USERS and USERS[username] == password:
       return True
    return False
