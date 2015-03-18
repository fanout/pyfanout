import sys
import unittest
import fanout

class TestJsonObjectFormat(unittest.TestCase):
	def test_initialize(self):
		format = JsonObjectFormat('value')
		self.assertEqual(format.value, 'value');

	def test_name(self):
		format = JsonObjectFormat('value')
		self.assert_equal(format.name(), 'json-object');

	def test_export(self):
		format = JsonObjectFormat('value')
		self.assertEqual(format.export(), 'value');

if __name__ == '__main__':
		unittest.main()
