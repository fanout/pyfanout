PyFanout
--------
Author: Justin Karneges <justin@fanout.io>

Fanout.io library for Python.

Requirements
------------

* PyJWT
* pubcontrol

Install
-------

You can install from PyPi:

    sudo pip install fanout

Or from this repository:

    sudo python setup.py install

Sample usage
------------

```python
import fanout

fanout.realm = 'my-realm-id'
fanout.key = 'my-realm-key'

fanout.publish('some-channel', 'hello')
```
