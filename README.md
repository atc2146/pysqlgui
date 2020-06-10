# :zap: Pysqlgui
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/atc2146/pysqlgui/blob/master/LICENSE.txt) [![Generic badge](https://img.shields.io/badge/made_with-python-blue.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/open_source-awesome-success.svg)](https://github.com/atc2146)   
  
**Pysqlgui** is a *lightweight* package for interfacing intuitively with SQL in Python.

## :books: Features

  - Run *any* valid SQL query.
  - Clean and **visually appealing** query results with column names.
  - Import tables from CSV files or Pandas DataFrames. 
  - Easily rename, create, or drop tables without writing long and complex queries.
  - Easily retrieve table information such as column type, default values, null constraints, and key constraints.
  - Helpful error messages.
  - And more!


## :memo: Usage

Using Pysqlgui is **easy**!

```python
import pysqlgui

stores = pysqlgui.Database(['customers.csv'], ['CUSTOMERS'])

stores.run_query('SELECT * FROM CUSTOMERS;')

```

In the example above, I created a database called stores and imported data from the customers.csv file and named the table CUSTOMERS.  Note: you can pass other data formats or no data at all!


## :desktop_computer: Installation

From [PyPi](https://pypi.org/project/pysqlgui "A lightweight and intuitive package to interface with SQL in Python."):

```python
pip install pysqlgui
```


## :book: Quick Guide 

Instantiate a Database object and pass any data if you wish.

```python
your_database_name = pysqlgui.Database()
```
Then call any of the methods below!


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

## :page_facing_up: Detailed Documentation

```python
pysqlgui.Database(data=None, table_names=None, name=None)
```


## :gear: Development

Pysqlgui is built on the [sqlite3](https://docs.python.org/3/library/sqlite3.html) standard library.  

The sqlite3 [Connection Object](https://docs.python.org/3/library/sqlite3.html#cursor-objects) and [Cursor Object](https://docs.python.org/3/library/sqlite3.html#cursor-objects) is available to you:

```python
Database.connection
Database.cursor
```

## :pencil2: Contributing

* Raise an [issue](https://github.com/atc2146/pysqlgui/issues) if you encounter any bugs or would like any features.
* Complete [function stubs](/pysqlgui/core_database.py).
* Write [tests](/tests/tests.py).

## :copyright: License

MIT © 2020 Alexander Chung

