import unittest
from base64 import b64decode
from pubcontrol import PubControl, Item
import fanout

class PubControlTestClass:
	def __init__(self):
		self.publish_channel = None
		self.publish_item = None
		self.publish_callback = None

	def publish(self, channel, item, blocking=False, callback=None):
		self.publish_channel = channel
		self.publish_item = item
		self.publish_blocking = blocking
		self.publish_callback = callback

class TestFanout(unittest.TestCase):
	def setUp(self):
		fanout._pubcontrols = dict()
		fanout.realm = None
		fanout.key = None
		fanout.ssl = True

	def test_initialize(self):
		self.assertEqual(fanout.realm, None)
		self.assertEqual(fanout.key, None)
		self.assertEqual(fanout.ssl, True)

	def test_initialize_with_params(self):
		fanout.realm = 'realm'
		fanout.key = 'key'
		fanout.ssl = 'ssl'
		self.assertEqual(fanout.realm, 'realm')
		self.assertEqual(fanout.key, 'key')
		self.assertEqual(fanout.ssl, 'ssl')

	def test_get_pubcontrol_error(self):
		with self.assertRaises(AssertionError):
			fanout._get_pubcontrol()

	def test_get_pubcontrol_existing(self):
		orig_pc = PubControl()
		fanout._pubcontrols[('realm', 'key', 'ssl')] = orig_pc
		fanout.realm = 'realm'
		fanout.key = 'key'
		fanout.ssl = 'ssl'	
		pc = fanout._get_pubcontrol()
		self.assertEqual(pc, orig_pc)

	def test_get_pubcontrol_new_http(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = False
		pc = fanout._get_pubcontrol()
		self.assertEqual(pc.clients[0].auth_jwt_claim, { 'iss': 'realm'})
		self.assertEqual(pc.clients[0].auth_jwt_key, b64decode('key=='))
		self.assertEqual(pc.clients[0].uri, 'http://api.fanout.io/realm/realm')

	def test_get_pubcontrol_new_https(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True	
		pc = fanout._get_pubcontrol()
		self.assertEqual(pc.clients[0].auth_jwt_claim, { 'iss': 'realm'})
		self.assertEqual(pc.clients[0].auth_jwt_key, b64decode('key=='))
		self.assertEqual(pc.clients[0].uri, 'https://api.fanout.io/realm/realm')

	def test_get_pubcontrol_get_specified(self):
		pc = fanout._get_pubcontrol('realm', 'key==', True)
		self.assertEqual(pc.clients[0].auth_jwt_claim, { 'iss': 'realm'})
		self.assertEqual(pc.clients[0].auth_jwt_key, b64decode('key=='))
		self.assertEqual(pc.clients[0].uri, 'https://api.fanout.io/realm/realm')

	def test_get_pubcontrol_get_multiple_specified(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True	
		orig_pc = fanout._get_pubcontrol()
		self.assertEqual(orig_pc.clients[0].auth_jwt_claim, { 'iss': 'realm'})
		self.assertEqual(orig_pc.clients[0].auth_jwt_key, b64decode('key=='))
		self.assertEqual(orig_pc.clients[0].uri, 'https://api.fanout.io/realm/realm')
		new_pc = fanout._get_pubcontrol('realm2', 'key==2', False)
		self.assertEqual(new_pc.clients[0].auth_jwt_claim, { 'iss': 'realm2'})
		self.assertEqual(new_pc.clients[0].auth_jwt_key, b64decode('key==2'))
		self.assertEqual(new_pc.clients[0].uri, 'http://api.fanout.io/realm/realm2')
		self.assertEqual(orig_pc, fanout._get_pubcontrol())

	def test_publish(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True
		pc = PubControlTestClass()
		fanout._pubcontrols[('realm', 'key==', True)] = pc
		fanout.publish('channel', 'item')
		self.assertEqual(pc.publish_channel, 'channel')
		self.assertEqual(pc.publish_item.export(), 
				Item(fanout.JsonObjectFormat('item')).export())
		self.assertEqual(pc.publish_blocking, False)

	def test_publish_with_custom_realm1(self):
		pc = PubControlTestClass()
		fanout._pubcontrols[('realm2', 'key==2', False)] = pc
		fanout.publish('channel', 'item', realm='realm2',
				key='key==2', ssl=False)
		self.assertEqual(pc.publish_channel, 'channel')
		self.assertEqual(pc.publish_item.export(), 
				Item(fanout.JsonObjectFormat('item')).export())
		self.assertEqual(pc.publish_blocking, False)

	def test_publish_with_custom_realm2(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True
		pc = PubControlTestClass()
		fanout._pubcontrols[('realm2', 'key==2', False)] = pc
		fanout.publish('channel', 'item', realm='realm2',
				key='key==2', ssl=False)
		self.assertEqual(pc.publish_channel, 'channel')
		self.assertEqual(pc.publish_item.export(), 
				Item(fanout.JsonObjectFormat('item')).export())
		self.assertEqual(pc.publish_blocking, False)

	def test_publish_blocking(self):
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True
		pc = PubControlTestClass()
		fanout._pubcontrols[('realm', 'key==', True)] = pc
		fanout.publish('channel', 'item', None, None, True)
		self.assertEqual(pc.publish_channel, 'channel')
		self.assertEqual(pc.publish_item.export(), 
				Item(fanout.JsonObjectFormat('item')).export())
		self.assertEqual(pc.publish_callback, None)
		self.assertEqual(pc.publish_blocking, True)

	def callback_for_testing(self, result, error):
		self.assertEqual(self.has_callback_been_called, False)
		self.assertEqual(result, False)
		self.assertEqual(error, 'error')
		self.has_callback_been_called = True

	def test_publish_with_callback(self):
		self.has_callback_been_called = False
		fanout.realm = 'realm'
		fanout.key = 'key=='
		fanout.ssl = True
		pc = PubControlTestClass()
		fanout._pubcontrols[('realm', 'key==', True)] = pc
		fanout.publish('channel', 'item', 'id', 'prev-id', False,
				self.callback_for_testing)
		self.assertEqual(pc.publish_channel, 'channel')
		self.assertEqual(pc.publish_item.export(),
				Item(fanout.JsonObjectFormat('item'), 'id', 'prev-id').export())
		self.assertEqual(pc.publish_blocking, False)
		pc.publish_callback(False, 'error')
		self.assertTrue(self.has_callback_been_called)

if __name__ == '__main__':
		unittest.main()
