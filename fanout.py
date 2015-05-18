#    fanout.py
#    ~~~~~~~~~
#    This module implements the Fanout functionality.
#    :authors: Justin Karneges, Konstantin Bokarius.
#    :copyright: (c) 2015 by Fanout, Inc.
#    :license: MIT, see LICENSE for more details.

from base64 import b64decode
import threading
from pubcontrol import PubControl, Item, Format
import threading

# The Fanout module is used for publishing messages to Fanout.io and is
# configured with a Fanout.io realm and associated key. SSL can either
# be enabled or disabled. Note that unlike the PubControl class
# there is no need to call the finish method manually, as it will
# automatically be called when the calling program exits.

# The realm, key, and SSL global configuration parameters used to configure
# this module.
realm = None
key = None
ssl = True

# The PubControl instance and lock used for synchronization.
_pubcontrols = dict()
_lock = threading.Lock()

# The JSON object format used for publishing messages to Fanout.io.
class JsonObjectFormat(Format):

	# Initialize with a value representing the message to be sent.
	def __init__(self, value):
		self.value = value

	# The name of the format.
	def name(self):
		return 'json-object'

	# The method used to export the format data.
	def export(self):
		return self.value

# An internal method used for retrieving the PubControl instance for the
# specified realm, key, and SSL values. If no values are specified then
# the global values are used. The PubControl instance is saved and if an
# instance is not available when this method is called then one will be
# created.
def _get_pubcontrol(realm=None, key=None, ssl=True):
	if realm is None and key is None:
		realm = globals()['realm']
		key = globals()['key']
		ssl = globals()['ssl']
	assert(realm)
	assert(key)
	_lock.acquire()
	if (realm, key, ssl) not in _pubcontrols:
		if ssl:
			scheme = 'https'
		else:
			scheme = 'http'
		_pubcontrols[(realm, key, ssl)] = PubControl({
			'uri': '%s://api.fanout.io/realm/%s' % (scheme, realm),
			'iss': realm,
			'key': b64decode(key)
		})
	_lock.release()
	return _pubcontrols[(realm, key, ssl)]

# Publish the specified data to the specified channel for the configured
# Fanout.io realm. The blocking parameter indicates whether the call should
# be blocking or non-blocking. Optionally provide an ID and previous ID to
# send along with the message, as well a callback method that will be called 
# after publishing is complete and passed the result and error message if an
# error was encountered. Optionally specify realm, key, and SSL values if
# different than the global configuration parameters.
def publish(channel, data, id=None, prev_id=None, blocking=False, callback=None,
		realm=None, key=None, ssl=True):
	if realm and key:
		pub = _get_pubcontrol(realm, key, ssl)
	else:
		pub = _get_pubcontrol()
	pub.publish(channel, Item(JsonObjectFormat(data), id, prev_id), blocking=blocking, callback=callback)
