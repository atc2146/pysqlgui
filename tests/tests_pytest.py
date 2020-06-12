
from pysqlgui import core_database


def test_func_1():
	"""
	"""
	my_db = core_database.Database()
	assert my_db.name is None
	assert 1 == 1
	
def test_func_2():
	assert core_database.some_random_3() == 5