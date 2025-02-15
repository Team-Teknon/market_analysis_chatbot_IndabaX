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

    def overall_sales_summary(self, product_name):
        """
        Returns the overall sales summary for a product over time.

        Parameters
        ----------
        product_name : str
            The name of the product to filter the data.

        Returns
        -------
        dict
            Overall sales summary over time.
        """
        # Filter the data for the specified product
        if product_name == "All Products".lower():
            product_data = self.data
        else:
            product_data = self.data[self.data['Item Name'] == product_name]

        # Group by 'Period' and sum the sales value and volume
        overall_summary = product_data.groupby('Period').sum()[['Sales_Value', 'Sales_Volume(KG_LTRS)']]

        # Convert the summary to a dictionary
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
        # Ensure 'Sales_Value' column is numeric
        self.data['Sales_Value'] = pd.to_numeric(self.data['Sales_Value'], errors='coerce')

        # Filter out NaN values if any
        self.data = self.data.dropna(subset=['Sales_Value'])

        # Calculate top performing products
        top_products = self.data.groupby('Item Name')['Sales_Value'].sum().nlargest(top_n)

        return top_products.to_dict()

    def market_share_by_category(self):
        """
        Returns the market share by category.

        Returns
        -------
        dict
            Market share by category.
        """
        market_share = self.data.groupby('Category')['Sales_Value'].sum()
        return market_share.to_dict()
