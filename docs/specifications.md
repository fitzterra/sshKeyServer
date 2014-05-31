Specifications for sshKeyServer
===============================

## Abstract
The *sshKeyServer* will be used to store public SSH keys for users, on specific
hosts, within domins. The `user@host.domain` will uniquely identify the user and
also allow a hierarchical structure for storing keys: **domain/host/user/key**

It will also allow automatically adding/removing authorization for any key to
any know user, by updating the `.ssh/authorized_keys` file automatically on the
user account to which access is being given.

The server will consists of two componets:

* __REST API service__: Allows key management via an HTTP API
* __Web UI__: Will allow key management and reporting via a web UI. The web UI will
  use the REST API for direct key management.

## REST API
This API will allow _adding_, _deleting_ and _reporting_ of _keys_, _users_,
_hosts_ and _domains_ , and also managing remote `./ssh/authorized_keys` files.

------------------------------------------------------------------------------

### Error Handling

All HTTP errors will return details about the error as serialized object in the
response body.

The Error Structure in the body will have these key/values:

    {
		'status': '400 Bad Request'
		'msg': 'Duplicate username: foo'
		'errorInfo': Optional additional error details. API dependant.
		'tb': Traceback if CP global request.show_tracebacks is True
	}

------------------------------------------------------------------------------

### Data Transmission Serialization
All APIs return data in JSON format unless otherwise stated.
All APIs supporting POST or PUT verbs, will allow the input data to be either
standard POST/PUT key=value pairs, or a JSON data structure containing the input
data.
If passing JSON data, the `Content-Type: application/json` header should be set.

------------------------------------------------------------------------------

### Authentication
All API **end points** will require authentication unless specifically stated
otherwise for any particular end point.

The authentication method will be
[**HTTP Digest Authentication**](http://tools.ietf.org/html/rfc2617.html RFC2617) 
as defined by [RFC2617](http://tools.ietf.org/html/rfc2617.html RFC2617).

------------------------------------------------------------------------------

### API End Points
All **end points** defined here are relative to a **baseURI** that will be
specific to each target server where the **sshKeyServer** will be running.

------------------------------------------------------------------------------

#### Direct Key Management
This is an endpoint for directly managing a key for a `user@host.domain` name.

__URI__: `{baseURI}/key/{user@host.domain}`

__Action__:

* **GET**: Retrieves the _publicKey_ for _user@host.domain_
	* __Authentication__: Not required.
    * __Success__: HTTP 200. The key is returned in the HTTP body
	* __Failure__: A 4xx error with details in the error structure

* **POST**: Adds a new _publicKey_ for _user@host.domain_
    * __Success__: HTTP 201. Empty body
	* __Failure__: A 4xx error with details in the error structure

* **PUT**: Replaces the current _publicKey_ for _user@host.domain_ with this new
  one.
	__?? How to handle authorized keys ??__
    * __Success__: HTTP 201. Empty body
	* __Failure__: A 4xx error with details in the error structure

* **DELETE**: Deletes the _publicKey_ for _user@host.domain_
	__?? How to handle authorized keys ??__
    * __Success__: HTTP 201. Empty body
	* __Failure__: A 4xx error with details in the error structure

------------------------------------------------------------------------------

### Managing remote `authorized_keys` files
?? How ??

