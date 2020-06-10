# Pysqlgui
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![Generic badge](https://img.shields.io/badge/made_with-python-blue.svg)](https://shields.io/)
**Pysqlgui** is a lightweight package for interfacing with SQL in Python.

## Features

  - Run any valid SQL query.
  - Import tables from CSV files or Pandas DataFrames. 
  - Clean and visually appealing query results with column names.
  - Easily rename, create, or drop tables without writing long and complex queries.
  - Easily retrieve table information such as column type, default values, null constraints, and key constraints.
  - Helpful error messages.
  - And more!

## Installation

From PyPi

```python
pip install pysqlgui
```

## Usage

Using Pysqlgui is easy!

```python
import pysqlgui

stores = pysqlgui.Database(['customers.csv'], ['CUSTOMERS'])

stores.run_query('SELECT * FROM CUSTOMERS;')
```

In the example above, I created a database called stores and imported data from the customers.csv file and named the table CUSTOMERS.  Note: you can pass other data formats or no data at all!





| Method | Summary |
| ------ | ------ |
| Database.run_query(query) | Run a SQL query. |
| Database.show(table_name) | Show the contents of a table. |
| Database.info(table_name=None) | Summary information about the database. Pass a table name as an argument to get table information. |
| Database.create_table(table_name, column_data) | Create an empty table. |
| Database.add_table(data, table_names=None) | Add a table to the database from a CSV file or Pandas DataFrame. |
| Database.insert_data(table_name, data) | Insert data into a table. |
| Database.drop_table(table_name) | Drop a table. |
| Database.rename_table(table_name) | Rename a table. |

### Examples

```python
pysqlgui.Database(data=None, table_names=None, name=None) | Create a database. 
```


## Development

Pysqlgui is built on the [sqlite3](https://docs.python.org/3/library/sqlite3.html) standard library.

The sqlite3 Connection Object and Cursor Object is available to you:

```python
Database.connection
Database.cursor
```

## Contributing

* Raise an issue if you encounter any bugs or would like any features.
* Complete function stubs.
* Write tests.

## License

MIT

