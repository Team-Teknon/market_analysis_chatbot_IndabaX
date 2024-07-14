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
        unit_price_comparison = city_data.groupby(['City', 'Period']).mean()['Unit_Price'].unstack()
        return unit_price_comparison.to_dict()

    def calculate_highest_average_sales_manufacturer(self, city_list):
        """
        Calculates the manufacturer with the highest average sales between specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        str
            Manufacturer with the highest average sales between specified cities.
        """
        # Filter data for specified cities
        city_data = self.data[self.data['City'].isin(city_list)]

        # Group by 'Manufacturer' and calculate average sales
        average_sales_by_manufacturer = city_data.groupby('Manufacturer')['Sales'].mean()

        # Find the manufacturer with the highest average sales
        highest_average_sales_manufacturer = average_sales_by_manufacturer.idxmax()

        return highest_average_sales_manufacturer

    def compare_sales_channel(self, city_list):
        """
        Compares the most effective sales channels considering the sales value for a list of cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            The most effective sales channels for the specified cities based on sales value.
        """
        # Filter data for the specified cities
        city_data = self.data[self.data['City'].isin(city_list)]

        # Group data by city and channel, then sum the sales value
        channel_sales = city_data.groupby(['City', 'Channel']).sum()['Sales_Value'].unstack()

        # Determine the channel with the highest sales value for each city
        most_effective_channels = channel_sales.idxmax(axis=1)

        # Filter to return only the results for the specified cities
        return most_effective_channels.loc[city_list].to_dict()

    def highest_sales_brand(self, city_list):
        """
        Determines the brand with the highest sales value amongst the specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            The brand with the highest sales value in each of the specified cities.
        """
        # Filter data for the specified cities
        city_data = self.data[self.data['City'].isin(city_list)]

        # Group data by city and brand, then sum the sales value
        brand_sales = city_data.groupby(['City', 'Brand']).sum()['Sales_Value'].unstack()

        # Determine the brand with the highest sales value for each city
        highest_sales_brands = brand_sales.idxmax(axis=1)

        # Filter to return only the results for the specified cities
        return highest_sales_brands.loc[city_list].to_dict()

    def highest_volume_packaging(self, city_list):
        """
        Determines the packaging type with the highest volume in the specified cities.

        Parameters
        ----------
        city_list : list of str
            The list of cities to compare.

        Returns
        -------
        dict
            The packaging type with the highest volume in each of the specified cities.
        """
        # Filter data for the specified cities
        city_data = self.data[self.data['City'].isin(city_list)]

        # Group data by city and packaging type, then sum the volume
        packaging_volume = city_data.groupby(['City', 'Pack_Size']).sum()['Volume'].unstack()

        # Determine the packaging type with the highest volume for each city
        highest_volume_packaging = packaging_volume.idxmax(axis=1)

        # Filter to return only the results for the specified cities
        return highest_volume_packaging.loc[city_list].to_dict()



