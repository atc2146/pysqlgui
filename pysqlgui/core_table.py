class Table:
    def __init__(self, df, name):
        """
        Parameters
        ----------
        df : Pandas DataFrame
            Pandas DataFrame representation of the table.
        
        name : str
            Name of the table.
        """
        self.df = df
        self.name = name
#         self.shape = self.get_shape() # rows, cols
               
    def get_shape(self): #OTHER WAY TO code this?, i.e self.shape is useless right now
        return self.df.shape
    
#     def alter(self):
#         pass
    
#     def insert(self):
#         pass
    
#     def delete(self):
#         pass