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

```sh
$ pip install pysqlgui
```

Upgrade to latest version 1.0.1 (Released June 14, 2020)
```sh
$ pip install pysqlgui --upgrade
```


## :book: Quick Guide

[Instantiate a Database object](https://github.com/atc2146/pysqlgui#page_facing_up-detailed-documentation) and pass any data if you wish.

```python
your_database_name = pysqlgui.Database()
```
Then call any of the methods below!


| Method | Summary |
| --------- | ------ |
| `Database.run_query(query)` | [Run a SQL query.](https://github.com/atc2146/pysqlgui#run-a-sql-query) |
| `Database.show(table_name)` | [Show the contents of a table.](https://github.com/atc2146/pysqlgui#show-table) |
| `Database.info(table_name=None)` | [Summary information](https://github.com/atc2146/pysqlgui#summary-information-about-the-database) about the database. Pass a table name as an argument to get table information. |
| `Database.create_table(table_name, column_data)` | [Create an empty table.](https://github.com/atc2146/pysqlgui#create-an-empty-table) |
| `Database.add_table(data, table_names=None)` | [Add a table](https://github.com/atc2146/pysqlgui#add-a-table) to the database from a CSV file or Pandas DataFrame. |
| `Database.insert_data(table_name, data)` | [Insert data into a table.](https://github.com/atc2146/pysqlgui#insert-data) |
| `Database.drop_table(table_name)` | [Drop a table.](https://github.com/atc2146/pysqlgui#drop-a-table) |
| `Database.rename_table(table_name, change_to)` | [Rename a table.](https://github.com/atc2146/pysqlgui#rename-a-table) |

## :page_facing_up: Detailed Documentation


#### Creating a database
```python
pysqlgui.Database(data=None, table_names=None, name=None)
```
**Parameters**  
* **data** : *list or dict*, default=None, Optional
    * Can be a list (of filepaths to CSVs, or of Pandas DataFrames), or a dict where the key is the table name and the value is the filepath to the CSV or a Pandas DataFrame.
* **table_names** : *list*, default=None, Optional
    * List of names of the tables, must be provided if data is of type list.
* **name** : *str*, default=None, Optional
    * Name given to the database.

```python
import pysqlgui as psg
import pandas as pd

# empty database
db_example_1 = psg.Database()

# from csv file via list notation
db_example_2 = psg.Database(['customers.csv'], ['CUSTOMERS'])

# from csv file via dict notation
db_example_3 = psg.Database({'CUSTOMERS': 'customers.csv'})

# from a Pandas DataFrame
df = pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})
db_example_4 = psg.Database([df], ['USERS'])

# from a combination
db_example_5 = psg.Database([df, 'customers.csv'], ['USERS', 'CUSTOMERS'])
db_example_6 = psg.Database({'CUSTOMERS': 'customers.csv', 'USERS': df})
```

---

#### Run a SQL query
```python
pysqlgui.Database.run_query(query)
```
Runs a SQL query.  

**Parameters**
* **query** : *str*
    * A SQL query.  

**Returns**
* **Pandas DataFrame, or None**
    * Returns a Pandas DataFrame if the query is of SELECT or PRAGMA type, None otherwise. Note, all valid SQL is allowed including CREATE, INSERT, DROP, etc.

```python
import pysqlgui as psg
import pandas as pd

# SELECT data
df = pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})
my_db = psg.Database([df], ['USERS'])
my_db.run_query('SELECT * FROM USERS;')
```

---

#### Show table
```python
pysqlgui.Database.show(table_name)
```
Shows the contents of a table. Equivalent to SELECT * FROM.    

**Parameters**
* **table_name** : *str*
    * The table to show.  

**Returns**
* **Pandas DataFrame**
    * Pandas DataFrame of the table contents.

```python
import pysqlgui as psg
import pandas as pd

my_db = core_database.Database([pd.DataFrame([['tom', 10], ['bob', 15]], columns=['name', 'age'])],['USERS'])
my_db.show('USERS')

```

---

#### Summary information about the database
```python
pysqlgui.Database.info(table_name=None)
```
Returns summary information about the database or a table.  

**Parameters**
* **table_name** : *str*, default=None, Optional  
    * The name of the table.  If a name is not provided, returns summary information about the database.  

**Returns**
* **Pandas DataFrame**
    * Returns summary database or table information in a Pandas DataFrame.

```python
import pysqlgui as psg
import pandas as pd

df = pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})
my_db = psg.Database([df], ['USERS'])

my_db.info() # database info
my_db.info('USERS') # table info
```

---

#### Create an empty table
```python
pysqlgui.Database.create_table(table_name, column_data)
```
Creates an empty table in the database. See [SQLite Datatypes](https://www.sqlite.org/datatype3.html).    

**Parameters**
* **table_name** : *str*   
    * The name of the table to be created.  

* **column_data** : *dict*   
    * Keys are the column names, and values are the type with any properties.  

**Returns**
* **None**

```python
import pysqlgui as psg
import pandas as pd

my_db = psg.Database()
my_db.create_table('users',
                    {'user_id': 'INTEGER',
                    'first_name': 'TEXT',
                    'join_date': 'DATE',
                    'score': 'FLOAT'})

# create tables with additional properties
my_db_2 = psg.Database()
my_db_2.create_table('users',
                    {'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                    'first_name': 'TEXT',
                    'join_date': 'DATE'})
my_db_2.create_table('articles',
                    {'article_id': 'INTEGER PRIMARY KEY',
                    'article_name': 'TEXT',
                    'written_by': 'INTEGER REFERENCES users(user_id)'})

```

---

#### Add a table
```python
pysqlgui.Database.add_table(data, table_names=None)
```
Adds one or more Table objects to the current Database instance.  

**Parameters**  
* **data** : *list or dict*
    * Can be a list (of filepaths to CSVs, or of Pandas DataFrames), or a dict where the key is the table name and the value is the filepath to the CSV or a Pandas DataFrame.
* **table_names** : *list*, default=None, Optional
    * List of names of the tables, must be provided if data is of type list.

**Returns**
* **None**

```python
import pysqlgui as psg
import pandas as pd

my_db = psg.Database()
df = pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})
my_db.add_table([df], ['USERS'])
```
---

#### Insert data
```python
pysqlgui.Database.insert_data(table_name, data)
```
Inserts data into the table.  Highly recommended to add via Pandas DataFrame.

**Parameters**  
* **table_name** : *str*
    * The name of the existing table to add data.
* **data** : *Pandas DataFrame or dict*
    * Pandas DataFrame with the corresponding columns.  Or a dict where keys are the column names, and values are the column value.

**Returns**
* **None**

```python
import pysqlgui as psg
import pandas as pd

my_db = psg.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'])

my_db.insert_data('USERS', pd.DataFrame({'name': ['Bob', 'Simram'], 'age': [22, 5]}))
my_db.insert_data('USERS', {'name': 'Jordan', 'age': 23})

```



---

#### Drop a table
```python
pysqlgui.Database.drop_table(table_name)
```
Drops a table in the database.  

**Parameters**  
* **table_name** : *str*
    * The name of the table to be dropped.

**Returns**
* **None**

```python
import pysqlgui as psg
import pandas as pd

my_db = psg.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'],
                     'MY_DB_NAME')
my_db.drop_table('USERS')
```

---

#### Rename a table
```python
pysqlgui.Database.rename_table(table_name, change_to)
```
Renames a table in the database.  

**Parameters**  
* **table_name** : *str*
    * The name of the table to be renamed.
* **change_to** : *str*
    * The new name of the table.

**Returns**
* **None**

```python
import pysqlgui as psg
import pandas as pd

my_db = psg.Database([pd.DataFrame({'name': ['John', 'Mary'], 'age': [32, 18]})],
                     ['USERS'],
                     'MY_DB_NAME')
my_db.rename_table('USERS', 'USERS_NEW_NAME')
```

---
Complete documentation coming very soon!

## :gear: Development

Pysqlgui is built on the [sqlite3](https://docs.python.org/3/library/sqlite3.html) standard library.  

The sqlite3 [Connection Object](https://docs.python.org/3/library/sqlite3.html#cursor-objects) and [Cursor Object](https://docs.python.org/3/library/sqlite3.html#cursor-objects) is available to you:

```python
Database.connection
Database.cursor
```

You can find sample data used for some of the examples [here](/examples).

## :pencil2: Contributing

* Raise an [issue](https://github.com/atc2146/pysqlgui/issues) if you encounter any bugs or would like any features.
* Complete [function stubs](/pysqlgui/core_database.py).
* Write [tests](/tests). See [instructions](/tests/how-to-run-tests-instructions.txt) on how to run tests.

**Clone the repo**

```sh
$ git clone https://github.com/atc2146/pysqlgui.git
```

## :copyright: License

[MIT](LICENSE.txt) © 2020 Alex Chung
