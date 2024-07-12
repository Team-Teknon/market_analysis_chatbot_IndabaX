import pandas as pd

class SalesPerformanceComparison:
    """
    A class used to compare sales performance across different cities.

    Attributes
    ----------
    data : pandas.DataFrame
        A DataFrame containing the sales data.

    Methods
    -------
    compare_sales_value(city_list)
    compare_sales_volume(city_list)
    compare_unit_price(city_list)
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the SalesPerformanceComparison object.

        Parameters
        ----------
        data : pandas.DataFrame
            The sales data.
        """
        self.data = data

    def compare_sales_value(self, city_list):
        """
        Returns the sales value comparison across the specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            Sales value comparison across the specified cities.
        """
        city_data = self.data[self.data['City'].isin(city_list)]
        sales_value_comparison = city_data.groupby(['City', 'Period'])['Sales_Value'].sum().unstack()
        print(sales_value_comparison.to_dict())
        return sales_value_comparison.to_dict()

    def compare_sales_volume(self, city_list):
        """
        Returns the sales volume comparison across the specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            Sales volume comparison across the specified cities.
        """
        city_data = self.data[self.data['City'].isin(city_list)]
        sales_volume_comparison = city_data.groupby(['City', 'Period']).sum()['Sales_Volume(KG_LTRS)'].unstack()
        return sales_volume_comparison.to_dict()

    def compare_average_unit_price(self, city_list):
        """
        Returns the average unit price comparison across the specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            Average unit price comparison across the specified cities.
        """
        city_data = self.data[self.data['City'].isin(city_list)]
    
        # Ensure 'Unit_Price' column is numeric
        city_data['Unit_Price'] = pd.to_numeric(city_data['Unit_Price'], errors='coerce')
        
        # Filter out rows where 'Unit_Price' is NaN
        city_data = city_data.dropna(subset=['Unit_Price'])
        
        # Verify that 'Unit_Price' is now numeric
        if not pd.api.types.is_numeric_dtype(city_data['Unit_Price']):
            raise ValueError("Unit_Price column must contain numeric values only.")
        
        # Calculate the mean unit price comparison
        unit_price_comparison = city_data.groupby(['City', 'Period'])['Unit_Price'].mean().unstack()
        
        return unit_price_comparison.to_dict()

