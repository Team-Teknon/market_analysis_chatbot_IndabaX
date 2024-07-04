import pandas as pd

class ProductSalesTrends:
    """
    A class used to analyze product sales trends over time.

    Attributes
    ----------
    data : pandas.DataFrame
        A DataFrame containing the sales data.

    Methods
    -------
    sales_over_time(product_name)
    sales_volume_over_time(product_name)
    average_unit_price_over_time(product_name)
    """
    def __init__(self, data):
        """
        Constructs all the necessary attributes for the ProductSalesTrends object.

        Parameters
        ----------
        data : pandas.DataFrame
            The sales data.
        """
        self.data = data
    
    def sales_over_time(self, product_name):
        """
        Returns the sales value over time for the specified product.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Sales value over time for the specified product.
        """
        product_data = self.data[self.data['Item Name'] == product_name]
        sales_over_time = product_data.groupby('Period').sum()['Sales_Value']
        return sales_over_time.to_dict()
    
    def sales_volume_over_time(self, product_name):
        """
        Returns the sales volume over time for the specified product.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Sales volume over time for the specified product.
        """
        product_data = self.data[self.data['Item Name'] == product_name]
        sales_volume_over_time = product_data.groupby('Period').sum()['Sales_Volume(KG_LTRS)']
        return sales_volume_over_time.to_dict()
    
    def average_unit_price_over_time(self, product_name):
        """
        Returns the average unit price over time for the specified product.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Average unit price over time for the specified product.
        """
        product_data = self.data[self.data['Item Name'] == product_name]
        average_unit_price_over_time = product_data.groupby('Period').mean()['Unit_Price']
        return average_unit_price_over_time.to_dict()