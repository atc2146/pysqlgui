import sqlite3
import pandas as pd
from pysqlgui.core_table import Table

class Database:
    
    def __init__(self, data=None, table_names=None, name=None):
        """
        Parameters
        ----------
        data : list or dict, default=None
            Can be a list (of filepaths to CSVs, or of Pandas DataFrames), or a dict
            where the key is the table name and the value is the filepath to the 
            CSV or a Pandas DataFrame.
        
        table_names : list, default=None
            List of names of the tables, must be provided if data is of type list.
        
        name : str, default=None
            Name given to the database.
        """
        self.connection = sqlite3.connect(":memory:")  # connection representing a database
        self.cursor = self.connection.cursor()
        
        self.name = name
        self.tables = []
        self.add_table(data, table_names)
        
    
    def get_table(self, table_name):
        """
        Returns a Table object if it exists in current Database instance.
        
        Parameters
        ----------
        table_name : str
            The name of the table to search for.
        
        Returns
        -------
        Table
            The corresponding Table object if it exists.
        """ 
        # check for str type?
        for table in self.tables:
            if table.name == table_name:
                return table
        raise ValueError(f'{table_name} table does not exist.')
    
    def remove(self, table):
        """
        Removes a Table object in the current Database instance.
        
        Parameters
        ----------
        table_name : str
            The name of the table to be removed.
               
        Returns
        -------
        None
        """
        try:
            self.tables.remove(table)
        except:
            raise ValueError(f'Could not remove table: {table}.')
            
    def summary(self):
        """
        Returns summary information about the database.
        
        Parameters
        ----------
        table_name : str
            The name of the table.
            
        Returns
        -------
        Returns information in a Pandas DataFrame
        """ 
        table_info = []
        
        for table in self.tables:
            rows, cols = table.get_shape()
            table_info.append([table.name, rows, cols])
            
        df = pd.DataFrame(table_info, columns=['Table Name', 'Rows', 'Columns'])
        
        return df
    
    def info(self, table_name=None):
        """
        Returns summary information about a table.
        
        Parameters
        ----------
        table_name : str
            The name of the table.
            
        Returns
        -------
        Returns information in a Pandas DataFrame
        """
        if table_name is None:
            return self.summary()
        else:
            try:
                df = self.run_query(f"PRAGMA TABLE_INFO({table_name});")
                df.rename(columns={'cid': 'Column ID',
                                      'name': 'Name',
                                      'type': 'Type',
                                      'notnull': 'Not NULL?',
                                      'dflt_value': 'Default Value',
                                      'pk': 'Primary Key?'
                                     }, inplace=True)

                df['Not NULL?'].replace(to_replace= {0: False, 1: True}, inplace=True)
                df['Primary Key?'].replace(to_replace= {0: 'No', 1: 'Yes'}, inplace=True)
                return df
            except:
                raise ValueError(f'Could not get table information.')
            
    def run_query(self, query: str):
        """
        Runs a SQL query.
        
        Parameters
        ----------
        query : str
            A SQL query.
        
        Returns
        -------
        A Pandas DataFrame if the query is of SELECT or PRAGMA type, None otherwise.
        """ 
        if query.lstrip().upper().startswith("SELECT") or query.lstrip().upper().startswith("PRAGMA"):
            return self.select(query)
        else:
            try:
                self.cursor.executescript(query)
                self.connection.commit()
                print(f'Successfully ran query: {query}.') # Might want to slice this when displaying
            except:
                raise ValueError(f'Could not run query: {query}.')
        
    def select(self, query: str):
        """
        Returns a Pandas DataFrame representation of a query.
        
        Parameters
        ----------
        query : str
            A SQL query.
        
        Returns
        -------
        Pandas DataFrame        
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall() # result is list of tuples
            column_names = list(map(lambda x: x[0], self.cursor.description))
            df = pd.DataFrame(data=result, columns=column_names)
            return df
        except:
            raise ValueError(f'ValueError - Could not execute given query: {query}')

    #allow strings?
    def add_table(self, data, table_names=None):
        """
        Adds one or more Table objects to the current Database instance.
        
        Parameters
        ----------
        data : list or dict
            Can be a list (of filepaths to CSVs, or of Pandas DataFrames), or a dict
            where the key is the table name and the value is the filepath to the 
            CSV or a Pandas DataFrame.
        
        table_names : list, default=None
            List of names of the tables, must be provided if data is of type list.
        
        Returns
        -------
        None
        """
        tables_dict = dict()
        
        if table_names is None:
            table_names = []
        
        if not data:
            # data is empty
            pass
        elif isinstance(data, dict):
            if len(data)<=len(table_names):
                for table, table_name in zip(data.items(), table_names):
                    tables_dict[table_name] = table[1]
            else:
                tables_dict = data
            # Note if more table_names are given than there are tables, the extra
            # table_names are ignored.  If there are less table_names given than there
            # are tables and tables is a dict, then all table_names are ignored
        
        elif isinstance(data, list) and isinstance(table_names, list):
            if len(data)<=len(table_names):
                 tables_dict = dict(zip(table_names, data))
            else:
                raise ValueError(f"Size mismatch - expected length of {len(data)} table_names, got {len(table_names)}.")
            # Note if more table_names are given than there are tables, the extra
            # table_names are ignored
        else:
            raise TypeError(f"""TypeError - expected list() or dict()""")
        
        
        for name, table in tables_dict.items():
            if not isinstance(name, str):
                raise TypeError(f"""TypeError - table name expected str, got {type(name)}""")
            if not isinstance(table, pd.DataFrame):
                # assume CSV, FIX for other types?
                table = pd.read_csv(table)                   

            table.to_sql(name, con=self.connection, index=False)
            self.tables.append(Table(table, name))

    def rename_table(self, table_name, change_to):
        """
        Renames a table in the database.
        
        Parameters
        ----------
        table_name : str
            The name of the table to be renamed.
        
        change_to : str
            The new name of the table.
        
        Returns
        -------
        None
        """        
        
        # check for valid table names
        if isinstance(change_to, str):
            if len(change_to) == 0:
                raise ValueError(f'Value error - expected len(change_to) > 0, got {len(change_to)}')
        else:
            raise TypeError(f'Type error - expected str, got {type(change_to)}')

        try:
            table = self.get_table(table_name)
            query = f'ALTER TABLE {table_name} RENAME TO {change_to};'
            self.run_query(query)
            table.name = change_to
            print(f'Successfully renamed {table_name} to {change_to}.')
        except:
            raise ValueError('Could not rename table.')
     
    def drop_table(self, table_name):
        """
        Drops a table in the database.
        
        Parameters
        ----------
        table_name : str
            The name of the table to be dropped.
               
        Returns
        -------
        None
        """     
        try:
            table = self.get_table(table_name)
            query = f'DROP TABLE {table_name};'
            self.run_query(query)
            self.remove(table)
            print(f'Successfully dropped {table_name}.')
        except:
            raise ValueError(f'Could not DROP table: {table_name}')
            
    def create_table(self, table_name, column_data):
        """
        Creates an empty table in the database.
        
        Parameters
        ----------
        table_name : str
            The name of the table to be created.
            
        data : dict
            Keys are the column names, and values
            are the type with any properties.
            
        Returns
        -------
        None
        """        
        query_cols = ""
        count = 0
        for k, v in column_data.items():
            count += 1
            if count == len(some_dict):
                query_cols += k + " " + v
            else:
                query_cols += k + " " + v + ', '

        query = f"CREATE table {table_name}({query_cols});"
        self.run_query(query)
        print(f'Successfully CREATED {table_name}.')
        self.tables.append(Table(pd.DataFrame(), table_name))
    
    def insert_data(self, table_name, data):
        """
        Inserts data into the table. 
        
        Parameters
        ----------
        table_name : str
            The name of the table.
            
        data : dict or Pandas DataFrame
            Keys are the column names, and values
            are the column value.
            
        Returns
        -------
        None
        """
        
        # CLEAN THIS UP!
        if isinstance(data, dict):
            try:
                table = self.get_table(table_name)

                col_names, col_values = row_rep_query(data)

                query = f"INSERT INTO {table_name}({col_names}) VALUES ({col_values});"
                self.run_query(query)
                
                table.df = table.df.append(pd.DataFrame.from_records([data]), ignore_index = True) 
#                 print(f'Successfully INSERTED values into {table_name}.')

            except:
                raise ValueError('Could not INSERT values into table.')        
        elif isinstance(data, pd.DataFrame):
            try:
                table = self.get_table(table_name)
                
                records = data.to_dict(orient='records')
                query = ""
                for row in records:
                    col_names, col_values = row_rep_query(row)
                    row_query = f"INSERT INTO {table_name}({col_names}) VALUES ({col_values});"
                    query += row_query
                    
                self.run_query(query)
                table.df = table.df.append(data, ignore_index = True) 
#                 print(f'Successfully INSERTED values into {table_name}.')

            except:
                raise ValueError('Could not INSERT values into table.')          
        else:
            raise TypeError(f'TypeError - Expected data to be dict or Pandas.Dataframe, got {type(data)}.')  
        
        
        
        

    
    # TO DO - Show within a certain range only?
    def show(self, table_name):
        """
        Shows the contents of a table.
        
        Equivalent to SELECT * FROM
        
        Parameters
        ----------
        table_name : str
            The table to show.
        
        Returns
        -------
        Pandas DataFrame        
        """
        return self.select(f'SELECT * FROM {table_name};')

    
### HELPER FUNCTIONS - WHERE SHOULD I PUT THIS?

def row_rep_query(data):
    """
    Returns a row representation of an INSERT statement,
    given as a tuple of the INSERT (col_names) VALUES (col_values)

    Parameters
    ----------
    data : dict
        Keys are the column names, and values
        are the column value.

    Returns
    -------
    Tuple 
    """
    col_names = ''
    col_values = ''
    count = 0
    for k,v in data.items():
        count+=1
        if count==len(data):
            col_names += k
            col_values += stringify(v)   
        else:
            col_names += k + ', '
            col_values += stringify(v) + ', '
    return (col_names, col_values)
    
    
def stringify(item):
    """
    Returns a quoted string item if passed argument
    is a string, else returns a string representation
    of that argument.
    
    If passed argument is None, returns None.

    Parameters
    ----------
    item : Any type
        Item to be parsed.

    Returns
    -------
    str or None
    """
    
    if item is None: # THIS IS ACTUALLY NOT NEEDED? HMMMMM
        return 'NULL'
    elif isinstance(item, str):
        item = item.replace("'","''")
        return f"'{item}'"
    else:
        return str(item)
    
### TO DO - FUNCTION STUBS
    def right_join(self):
        pass
    
    def outer_join(self):
        pass
    
    def history(self):
        pass
    
    def truncate(self):
        pass