# :zap: Pysqlgui
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/atc2146/pysqlgui/blob/master/LICENSE.txt) [![Generic badge](https://img.shields.io/badge/made_with-python-blue.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/open_source-awesome-success.svg)](https://github.com/atc2146)<br> 
  
**Pysqlgui** is a *lightweight* package for interfacing intuitively with **SQL** in Python.<br>

## :books: Features

  - Run **_any_** valid SQL query.
  - Clean and **visually appealing** query results with column names.
  - Import tables from **CSV files** or **[Pandas DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)**. 
  - Easily **rename**, **create**, or **drop** tables without writing *long and complex* queries.
  - Easily retrieve table information such as **column type**, **default values**, **null constraints**, and **key constraints**.
  - Helpful **error messages**.
  - And **more**!


## :memo: Usage

Using Pysqlgui is **easy**!<br>

```python
import pysqlgui

# Load a file and name the table
stores = pysqlgui.Database(['customers.csv'], ['CUSTOMERS'])

# Run a query
stores.run_query('SELECT * FROM CUSTOMERS;')

```

If you are running code in a `Jupyter Notebook`, the output will be a Pandas DataFrame.  Otherwise, call print on the line above to print out the query result.

**_Note_**: you can pass other data formats or no data at all!  Refer to [detailed documentation](https://github.com/atc2146/pysqlgui#page_facing_up-detailed-documentation "Detailed Documentation") below.


## :desktop_computer: Installation

From **[PyPi](https://pypi.org/project/pysqlgui)**:

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
| --------- | ------ |
| `Database.run_query(query)` | Run a SQL query. |
| `Database.show(table_name)` | Show the contents of a table. |
| `Database.info(table_name=None)` | Summary information about the database. Pass a table name as an argument to get table information. |
| `Database.create_table(table_name, column_data)` | Create an empty table. |
| `Database.add_table(data, table_names=None)` | Add a table to the database from a CSV file or Pandas DataFrame. |
| `Database.insert_data(table_name, data)` | Insert data into a table. |
| `Database.drop_table(table_name)` | Drop a table. |
| `Database.rename_table(table_name)` | Rename a table. |

## :page_facing_up: Detailed Documentation


#### Creating a Database
```python 
pysqlgui.Database(data=None, table_names=None, name=None)
```
**Parameters**  

* **data** : *list or dict*, default=None
    * Can be a list (of filepaths to CSVs, or of Pandas DataFrames), or a dict where the key is the table name and the value is the filepath to the CSV or a Pandas DataFrame.
* **table_names** : *list*, default=None
    * List of names of the tables, must be provided if data is of type list.
* **name** : *str*, default=None
    * Name given to the database.

Complete documentation coming very soon!

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

MIT © 2020 Alex Chung

