#    fanout.py
#    ~~~~~~~~~
#    This module implements the Fanout functionality.
#    :authors: Justin Karneges, Konstantin Bokarius.
#    :copyright: (c) 2015 by Fanout, Inc.
#    :license: MIT, see LICENSE for more details.

from base64 import b64decode
import threading
import atexit
from pubcontrol import PubControl, Item, Format

# The Fanout module is used for publishing messages to Fanout.io and is
# configured with a Fanout.io realm and associated key. SSL can either
# be enabled or disabled. As a convenience, the realm and key
# can also be configured by setting the 'FANOUT_REALM' and 'FANOUT_KEY'
# environmental variables. Note that unlike the PubControl class
# there is no need to call the finish method manually, as it will
# automatically be called when the calling program exits.

# The realm, key, and SSL configuration parameters used to configure
# this module.
realm = None
key = None
ssl = True

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

_threadlocal = threading.local()

# An internal method used for retrieving the PubControl instance. The
# PubControl instance is saved as a thread variable and if an instance
# is not available when this method is called then one will be created.
def _get_pubcontrol():
	assert(realm)
	assert(key)
	if not hasattr(_threadlocal, 'pubcontrol'):
		if ssl:
			scheme = 'https'
		else:
			scheme = 'http'
		pub = PubControl({
			'uri': '%s://api.fanout.io/realm/%s' % (scheme, realm),
			'iss': realm,
			'key': b64decode(key)
		})
		atexit.register(pub.finish)
		_threadlocal.pubcontrol = pub
	return _threadlocal.pubcontrol

# Asynchronously publish the specified data to the specified channel for
# the configured Fanout.io realm. The blocking parameter indicates whether
# the call should be blocking or non-blocking. Optionally provide an ID and
# previous ID to send along with the message, as well a callback method that
# will be called after publishing is complete and passed the result and error
# message if an error was encountered.
def publish(channel, data, id=None, prev_id=None, blocking=False, callback=None):
	pub = _get_pubcontrol()
	pub.publish(channel, Item(JsonObjectFormat(data), id, prev_id), blocking=blocking, callback=callback)
