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

def test_drop_table_when_no_tables_exist():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.drop_table("this_table_doesnt_exist")

def test_drop_table_when_no_tables_exist_empty_string():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.drop_table("")

def test_drop_table():
	df = pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])
	db = core_database.Database([df], ['table_1'])
	num_of_tables = len(db.tables)
	db.drop_table('table_1')
	assert num_of_tables == len(db.tables) + 1
	with pytest.raises(ValueError):
		db.get_table('table_1')

def test_create_table_empty_string():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.create_table('', {'user_id': 'INT'})

def test_create_table_incorrect_table_name_format():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.create_table(['not_a_string'], {'user_id': 'INT'})

def test_create_table_incorrect_column_data_format():
	db = core_database.Database()
	with pytest.raises(ValueError):
		db.create_table('not_a_string', [{'user_id': 'INT'}])

def test_create_table():
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.create_table('example_table', {'user_id': 'INTEGER',
              'first_name': 'TEXT',
               'join_date': 'DATE',
               'score': 'FLOAT'
              })
	assert num_of_tables == len(db.tables) - 1
	assert db.get_table('example_table').name == 'example_table'
	assert db.info().shape[0] == 1

def test_create_table_with_primary_key():
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.create_table('example_table', {'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
              'first_name': 'TEXT',
               'join_date': 'DATE',
               'score': 'FLOAT'
              })
	assert num_of_tables == len(db.tables) - 1
	assert db.get_table('example_table').name == 'example_table'
	assert db.info().shape[0] == 1

def test_create_table_with_primary_key_and_foreign_key():
	db = core_database.Database()
	num_of_tables = len(db.tables)
	db.create_table('example_table_1', {'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
              'first_name': 'TEXT',
               'join_date': 'DATE',
               'score': 'FLOAT'
              })
	db.create_table('example_table_2', {'food_id': 'INTEGER',
              'user_id': 'INTEGER REFERENCES example_table_1(user_id)'
              })
	assert num_of_tables == len(db.tables) - 2
	assert db.info().shape[0] == 2

def test_insert_data_pandas_dataframe():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	more_data = pd.DataFrame({'name': ['Bob', 'Simram'], 'age': [22, 5]})
	my_db.insert_data('USERS', more_data)
	assert my_db.show('USERS').shape[0] == 4

def test_insert_data_dict():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	my_db.insert_data('USERS', {'name': 'Bob', 'age': 22})
	assert my_db.show('USERS').shape[0] == 3

def test_insert_data_wrong_data_type():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	with pytest.raises(TypeError):
		my_db.insert_data('USERS', [{'name': 'Bob', 'age': 22}])

def test_insert_data_dict_wrong_column_name():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	with pytest.raises(ValueError):
		my_db.insert_data('USERS', {'WRONG_NAME': 'Bob', 'age': 22})

def test_insert_data_wrong_columns_in_new_data():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	more_data = pd.DataFrame({'name': ['Bob', 'Simram'], 'age': [22, 5], 'height': [170, 120]})
	with pytest.raises(ValueError):
		my_db.insert_data('USERS', more_data)

def test_insert_data_wrong_column_name_in_new_data():
	my_db = core_database.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])
	with pytest.raises(ValueError):
		my_db.insert_data('USERS', pd.DataFrame({'WRONG_NAME': ['Bob', 'Simram'], 'age': [22, 5]}))

def test_show():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	assert db.show('example_table').shape[0] == 3
	assert isinstance(db.show('example_table'), pd.DataFrame)

def test_show_non_existant_table():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	with pytest.raises(ValueError):
		db.show('not_an_existing_table_name')

def test_show_empty_table_name():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	with pytest.raises(ValueError):
		db.show('')

def test_show_table_name_not_a_string():
	db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15], ['juli', 14]], columns=['name', 'age'])],['example_table'])
	with pytest.raises(ValueError):
		db.show(['not_a_string'])
