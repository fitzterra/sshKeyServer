# -*- coding: utf-8 -*-
"""
Tests the API
"""

import requests
import hashlib

baseURI = "http://localhost:8091/api/key"
auth = ('admin', 'admin')

for host in range(5):
    for user in range(3):
        user = "user{0}@host{1}.tld".format(user, host)
        key = hashlib.md5(user).hexdigest()
        payload = {'key': key}
        r = requests.post("{0}/{1}".format(baseURI,user), data=payload,
                          auth=auth)
        if r.status_code != 201:
            print r.text
        else:
            print r.json()

