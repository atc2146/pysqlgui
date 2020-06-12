import unittest

from pysqlgui import core_database

class TestMethods(unittest.TestCase):

	def test_func_1(self):
		"""
		"""
		my_db = core_database.Database()
		assert my_db.name is None
		assert 1 == 0