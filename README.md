PyFanout
--------
Author: Justin Karneges <justin@fanout.io>

Fanout.io library for Python.

Requirements
------------

* jwt
* pubcontrol

Sample usage
------------

```python
import fanout

fanout.realm = 'my-realm-id'
fanout.key = 'my-realm-key'

fanout.publish('some-channel', 'hello')
```
