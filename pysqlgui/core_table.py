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
               
    def get_shape(self):
        """
        Returns
        -------
        Tuple(int, int)
            The shape of the Table (DataFrame)
        """
        return self.df.shape
