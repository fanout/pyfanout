from base64 import b64decode
import threading
import json
from pubcontrol import PubControl, Item, Format

realm = None
key = None
ssl = True

class FppFormat(Format):
	def __init__(self, value):
		self.value = value

	def name(self):
		return 'fpp'

	def export(self):
		return self.value

_threadlocal = threading.local()

def _get_pubcontrol():
	assert(realm)
	assert(key)
	if not hasattr(_threadlocal, "pubcontrol"):
		if ssl:
			scheme = 'https'
		else:
			scheme = 'http'
		pub = PubControl('%s://api.fanout.io/realm/%s' % (scheme, realm))
		pub.set_auth_jwt({ 'iss': realm }, b64decode(key))
		_threadlocal.pubcontrol = pub
	return _threadlocal.pubcontrol

def publish(channel, data, id=None, prev_id=None):
	pub = _get_pubcontrol()
	pub.publish(channel, Item(FppFormat(data), id, prev_id))

def publish_async(channel, data, id=None, prev_id=None, callback=None):
	pub = _get_pubcontrol()
	pub.publish_async(channel, Item(FppFormat(data), id, prev_id, callback))
