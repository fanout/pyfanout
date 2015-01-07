from base64 import b64decode
import threading
import atexit
from pubcontrol import PubControl, Item, Format

realm = None
key = None
ssl = True

class JsonObjectFormat(Format):
	def __init__(self, value):
		self.value = value

	def name(self):
		return 'json-object'

	def export(self):
		return self.value

_threadlocal = threading.local()

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

def publish(channel, data, id=None, prev_id=None, blocking=False, callback=None):
	pub = _get_pubcontrol()
	pub.publish(channel, Item(JsonObjectFormat(data), id, prev_id), blocking=blocking, callback=callback)
