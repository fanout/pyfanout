import sys
import unittest
import fanout

class TestJsonObjectFormat(unittest.TestCase):
	def test_initialize(self):
		format = fanout.JsonObjectFormat('value')
		self.assertEqual(format.value, 'value');

	def test_name(self):
		format = fanout.JsonObjectFormat('value')
		self.assertEqual(format.name(), 'json-object');

	def test_export(self):
		format = fanout.JsonObjectFormat('value')
		self.assertEqual(format.export(), 'value');

if __name__ == '__main__':
		unittest.main()
