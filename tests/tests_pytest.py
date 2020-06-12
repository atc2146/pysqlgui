import pytest

from pysqlgui import core_database
from pysqlgui.core_table import Table

import pandas as pd

def test_init_no_parameters():
	db = core_database.Database()
	assert hasattr(db, "connection")
	assert hasattr(db, "cursor")
	assert hasattr(db, "name")
	assert hasattr(db, "tables")
	assert db.name is None
	assert db.tables == []

def test_init_with_name_parameter_only():
	db = core_database.Database(None, None, "name_of_db")
	assert db.name == "name_of_db"
	assert isinstance(db.name, str)
	assert db.tables == []

def test_get_table_check_table_type():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	assert isinstance(db.get_table('example_table'), Table)

def test_get_table_on_non_existent_table():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.get_table('some_table_name_that_doesnt_exist')

def test_remove_on_non_existent_table():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.remove(Table(pd.DataFrame(), 'some_table_name_that_doesnt_exist'))

def test_remove_on_existent_table():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	t = db.get_table('example_table')
	assert isinstance(t, Table)
	assert db.remove(t) is None
	assert len(db.tables) == 0
