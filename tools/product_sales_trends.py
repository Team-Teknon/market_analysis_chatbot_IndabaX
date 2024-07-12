import pandas as pd
import numpy as np
from datetime import datetime, timedelta


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
        self.data['Month'] = self.data['Period'].dt.month
        self.data['Year'] = self.data['Period'].dt.year
        self.data['Week'] = self.data['Period'].dt.to_period('W')
        self.data['Season'] = self.data['Period'].dt.month % 12 // 3 + 1

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
        sales_over_time = product_data.groupby('Period')['Sales_Value'].sum()
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
        sales_volume_over_time = product_data.groupby('Period')['Sales_Volume(KG_LTRS)'].sum()
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
        average_unit_price_over_time = product_data.groupby('Period')['Unit_Price'].mean()
        return average_unit_price_over_time.to_dict()

    def product_sales_trends_by_period(self, product_name, period, month=None):
        """
        Calculate product sales trends based on the specified period.
        
        Args:
            product_name (str): The name of the product to calculate sales trends for.
            period (str): The period for which to calculate sales trends. 
                          Can be 'over_time', 'last_quarter', 'this_month', 'first_quarter', or 'custom_month'.
            month (int, optional): The month for which to calculate sales trends if period is 'custom_month'.
        
        Returns:
            dict: Sales trends for the specified period for the specified product.
        """
        product_data = self.data[self.data['Item Name'] == product_name]

        if period == 'over_time':
            filtered_data = product_data
        elif period == 'last_quarter':
            start_date = datetime.now() - timedelta(days=91)
            filtered_data = product_data[product_data['Period'] >= start_date]
        elif period == 'this_month':
            this_month = datetime.now().month
            this_year = datetime.now().year
            filtered_data = product_data[(product_data['Year'] == this_year) &
                                         (product_data['Month'] == this_month)]
        elif period == 'first_quarter':
            filtered_data = product_data[product_data['Month'].isin([1, 2, 3])]
        elif period == 'custom_month':
            if not month:
                raise ValueError("You must specify the month when period is 'custom_month'.")
            filtered_data = product_data[product_data['Month'] == month]
        else:
            raise ValueError("Invalid period specified. Choose from 'over_time', 'last_quarter', 'this_month', "
                             "'first_quarter', or 'custom_month'.")

        sales_trends = filtered_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def sales_in_month(self, month):
        """
        Calculate sales trends for a specific month.
        
        Args:
            month (int): The month for which to calculate sales trends (1 = January, 2 = February, etc.).
        
        Returns:
            dict: Sales trends for the specified month.
        """
        if month < 1 or month > 12:
            raise ValueError("Invalid month. Please specify a month between 1 and 12.")

        month_data = self.data[self.data['Month'] == month]
        sales_trends = month_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def product_sales_performance_last_year(self, product_name):
        """
        Returns the sales performance for a specific product over the last year.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Sales performance over the last year for the specified product.
        """
        one_year_ago = datetime.now() - timedelta(days=365)
        last_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'] >= one_year_ago)]
        sales_performance = last_year_data.groupby('Period')['Sales_Value'].sum()
        return sales_performance.to_dict()

    def weekly_sales_trends(self):
        """
        Returns the weekly sales trends.

        Returns
        -------
        dict
            Weekly sales trends.
        """
        weekly_trends = self.data.groupby('Week')['Sales_Value'].sum()
        return weekly_trends.to_dict()

    def compare_sales_trends(self, product_a, product_b):
        """
        Compares sales trends between two products.

        Parameters
        ----------
        product_a : str
            The name of the first product to compare.
        product_b : str
            The name of the second product to compare.

        Returns
        -------
        dict
            Sales trends comparison between the two products.
        """
        product_a_data = self.data[self.data['Item Name'] == product_a]
        product_b_data = self.data[self.data['Item Name'] == product_b]
        sales_trends_a = product_a_data.groupby('Period')['Sales_Value'].sum()
        sales_trends_b = product_b_data.groupby('Period')['Sales_Value'].sum()
        return {'Product A': sales_trends_a.to_dict(), 'Product B': sales_trends_b.to_dict()}

    def compare_sales_this_year_last_year(self, product_name):
        """
        Compares sales trends for a product between this year and last year.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Sales trends comparison for the specified product between this year and last year.
        """
        this_year = datetime.now().year
        last_year = this_year - 1
        this_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Year'] == this_year)]
        last_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Year'] == last_year)]
        sales_trends_this_year = this_year_data.groupby('Period')['Sales_Value'].sum()
        sales_trends_last_year = last_year_data.groupby('Period')['Sales_Value'].sum()
        return {'This Year': sales_trends_this_year.to_dict(), 'Last Year': sales_trends_last_year.to_dict()}

    def compare_product_to_overall(self, product_name):
        """
        Compares sales trends for a specific product to overall sales trends.

        Parameters
        ----------
        product_name : str
            The name of the product to compare.

        Returns
        -------
        dict
            Comparison between product sales trends and overall sales trends.
        """
        product_data = self.data[self.data['Item Name'] == product_name]
        overall_data = self.data.groupby('Period')['Sales_Value'].sum()
        product_sales_trends = product_data.groupby('Period')['Sales_Value'].sum()
        return {'Product': product_sales_trends.to_dict(), 'Overall': overall_data.to_dict()}

    def sales_in_region(self, region):
        """
        Returns sales trends for a specific region.

        Parameters
        ----------
        region : str
            The name of the region to analyze.

        Returns
        -------
        dict
            Sales trends for the specified region.
        """
        region_data = self.data[self.data['Region'] == region]
        sales_trends = region_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def sales_trends_past_year_region(self, region):
        """
        Returns sales trends for the past year in a specific region.

        Parameters
        ----------
        region : str
            The name of the region to analyze.

        Returns
        -------
        dict
            Sales trends for the past year in the specified region.
        """
        one_year_ago = datetime.now() - timedelta(days=365)
        region_data = self.data[(self.data['Region'] == region) & (self.data['Period'] >= one_year_ago)]
        sales_trends = region_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def product_sales_in_city_region(self, product_name, region):
        """
        Returns sales trends for a specific product in a specific region.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.
        region : str
            The name of the region to analyze.

        Returns
        -------
        dict
            Sales trends for the specified product in the specified region.
        """
        region_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Region'] == region)]
        sales_trends = region_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def monthly_sales_in_region(self, region):
        """
        Returns monthly sales trends for a specific region.

        Parameters
        ----------
        region : str
            The name of the region to analyze.

        Returns
        -------
        dict
            Monthly sales trends for the specified region.
        """
        region_data = self.data[self.data['Region'] == region]
        sales_trends = region_data.groupby('Month')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def seasonal_sales_trends(self):
        """
        Returns seasonal sales trends.

        Returns
        -------
        dict
            Seasonal sales trends.
        """
        seasonal_trends = self.data.groupby('Season')['Sales_Value'].sum()
        return seasonal_trends.to_dict()

    def product_sales_during_summer(self, product_name):
        """
        Returns sales trends for a specific product during summer.

        Parameters
        ----------
        product_name : str
            The name of the product to analyze.

        Returns
        -------
        dict
            Sales trends for the specified product during summer.
        """
        summer_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Month'].isin([6, 7, 8]))]
        sales_trends = summer_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def sales_second_quarter(self):
        """
        Returns sales trends for the second quarter.

        Returns
        -------
        dict
            Sales trends for the second quarter.
        """
        second_quarter_data = self.data[self.data['Month'].isin([4, 5, 6])]
        sales_trends = second_quarter_data.groupby('Period')['Sales_Value'].sum()
        return sales_trends.to_dict()

    def compare_sales_second_quarter(self):
        """
        Compares sales trends for the second quarter between this year and last year.

        Returns
        -------
        dict
            Comparison of sales trends for the second quarter between this year and last year.
        """
        this_year = datetime.now().year
        last_year = this_year - 1
        this_year_second_quarter = self.data[(self.data['Year'] == this_year) & (self.data['Month'].isin([4, 5, 6]))]
        last_year_second_quarter = self.data[(self.data['Year'] == last_year) & (self.data['Month'].isin([4, 5, 6]))]
        sales_trends_this_year = this_year_second_quarter.groupby('Period')['Sales_Value'].sum()
        sales_trends_last_year = last_year_second_quarter.groupby('Period')['Sales_Value'].sum()
        return {'This Year': sales_trends_this_year.to_dict(), 'Last Year': sales_trends_last_year.to_dict()}
