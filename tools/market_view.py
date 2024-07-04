import pandas as pd

class MarketView:
    """
    A class used to provide a holistic view of the market.

    Attributes
    ----------
    data : pandas.DataFrame
        A DataFrame containing the sales data.

    Methods
    -------
    overall_sales_summary()
        Returns the overall sales summary over time.
    top_performing_products(top_n=10)
        Returns the top performing products based on sales value.
    market_share_by_category()
        Returns the market share by category.
    """
    
    def __init__(self, data):
        """
        Constructs all the necessary attributes for the MarketView object.

        Parameters
        ----------
        data : pandas.DataFrame
            The sales data.
        """
        self.data = data

    def overall_sales_summary(self):
        """
        Returns the overall sales summary over time.

        Returns
        -------
        dict
            Overall sales summary over time.
        """
        overall_summary = self.data.groupby('Period').sum()[['Sales_Value', 'Sales_Volume(KG_LTRS)']]
        return overall_summary.to_dict()
    
    def top_performing_products(self, top_n=10):
        """
        Returns the top performing products based on sales value.

        Parameters
        ----------
        top_n : int, optional
            The number of top performing products to return (default is 10).

        Returns
        -------
        dict
            Top performing products based on sales value.
        """
        top_products = self.data.groupby('Item Name').sum()['Sales_Value'].nlargest(top_n)
        return top_products.to_dict()
    
    def market_share_by_category(self):
        """
        Returns the market share by category.

        Returns
        -------
        dict
            Market share by category.
        """
        market_share = self.data.groupby('Category').sum()['Sales_Value']
        return market_share.to_dict()
