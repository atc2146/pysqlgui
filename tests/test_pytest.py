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

def test_summary_on_existent_table():
	example_df = [pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])]
	db = core_database.Database(example_df, ['example_table'])
	df = db.summary()
	assert isinstance(df, pd.DataFrame)
	assert not df.empty
	assert list(df.columns.values) == ['Table Name', 'Rows', 'Columns']
	assert any(df['Table Name'] == 'example_table')
	assert df[df['Table Name'] == 'example_table']['Rows'].values[0] == 3
	assert df[df['Table Name'] == 'example_table']['Columns'].values[0] == 2

def test_info_on_existent_table_but_called_with_wrong_name():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	t = db.get_table('example_table')
	assert isinstance(t, Table)
	with pytest.raises(ValueError):
		db.info('table_does_not_exist')

def test_info_on_existent_table():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	t = db.get_table('example_table')
	assert isinstance(t, Table)
	df = db.info('example_table')
	assert isinstance(df, pd.DataFrame)
	assert set(list(df.columns.values)) == {'Column ID', 'Column Name', 'Type', 'Not NULL?', 'Default Value', 'Primary Key?'}
	assert all(df[df['Column Name'] == 'Primary Key?'])
	assert any(df[df['Column Name'] == 'age'])

def test_run_query_simple_select():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	assert isinstance(db.run_query('SELECT * FROM example_table'), pd.DataFrame)
	assert not db.run_query('SELECT * FROM example_table').empty

def test_run_query_with_pragma():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	assert isinstance(db.run_query('''PRAGMA TABLE_INFO('example_table')'''), pd.DataFrame)
	assert not db.run_query('''PRAGMA TABLE_INFO('example_table')''').empty

def test_run_query_wrong_syntax():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	with pytest.raises(ValueError):
		db.run_query('SELECT * FROMMMMM example_table')

def test_select_simple_query():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	assert not db.select('''SELECT * FROM example_table''').empty

def test_select_wrong_syntax():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	with pytest.raises(ValueError):
		db.select('SELECT * FROMMMMM example_table')

def test_add_table_valid_data_in_list_but_no_table_name():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.add_table([df])

def test_add_table_empty_data_no_table_name():
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.add_table(None, None)
	assert num_of_tables == len(db.tables)

def test_add_table_empty_data_with_table_name():
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.add_table(None, ['example_table'])
	assert num_of_tables == len(db.tables)

def test_add_table_but_wrong_agrument_types_1():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	with pytest.raises(TypeError):
		db.add_table([df], 'example_table')

def test_add_table_but_wrong_agrument_types_2():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	with pytest.raises(TypeError):
		db.add_table(df, 'example_table')

def test_add_table_but_wrong_agrument_types_3():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	with pytest.raises(TypeError):
		db.add_table(df, ['example_table'])

def test_add_table_valid_data_in_list_and_table_name_in_list():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.add_table([df], ['example_table'])
	assert num_of_tables == len(db.tables) - 1

def test_add_table_valid_data_in_dict():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.add_table({'example_table': df})
	assert num_of_tables == len(db.tables) - 1

def test_add_table_valid_data_in_dict_but_wrong_key_value_order():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database()
	with pytest.raises(TypeError):
		db.add_table({df: 'example_table'})

def test_rename_table():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database([df], ['table_1'])
	assert db.rename_table('table_1', 'table_1_new_name') is None
	assert db.get_table('table_1_new_name').name == 'table_1_new_name'

def test_rename_table_empty_string():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database([df], ['table_1'])
	with pytest.raises(ValueError):
		db.rename_table('table_1', '')

def test_rename_table_not_a_string():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database([df], ['table_1'])
	with pytest.raises(TypeError):
		db.rename_table('table_1', ['a_list'])

def test_rename_table_which_doesnt_exist():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database([df], ['table_1'])
	with pytest.raises(ValueError):
		db.rename_table('some_table_name_that_doesnt_exist', 'new_name')
