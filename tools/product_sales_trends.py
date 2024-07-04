import pandas as pd
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
    
    def sales_trends_past_year(self):
        one_year_ago = datetime.now() - timedelta(days=365)
        past_year_data = self.data[self.data['Period'] >= one_year_ago]
        sales_trends = past_year_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def sales_trends_last_six_months(self):
        six_months_ago = datetime.now() - timedelta(days=182)
        last_six_months_data = self.data[self.data['Period'] >= six_months_ago]
        sales_trends = last_six_months_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def sales_trends_this_year(self):
        this_year = datetime.now().year
        this_year_data = self.data[self.data['Period'].dt.year == this_year]
        sales_trends = this_year_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def product_sales_trends_over_time(self, product_name):
        product_data = self.data[self.data['Item Name'] == product_name]
        sales_trends = product_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def product_sales_trends_last_quarter(self, product_name):
        three_months_ago = datetime.now() - timedelta(days=91)
        last_quarter_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'] >= three_months_ago)]
        sales_trends = last_quarter_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def product_sales_trends_this_month(self, product_name):
        this_month = datetime.now().month
        this_year = datetime.now().year
        this_month_data = self.data[(self.data['Item Name'] == product_name) & 
                                    (self.data['Period'].dt.year == this_year) & 
                                    (self.data['Period'].dt.month == this_month)]
        sales_trends = this_month_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def product_sales_performance_last_year(self, product_name):
        one_year_ago = datetime.now() - timedelta(days=365)
        last_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'] >= one_year_ago)]
        sales_performance = last_year_data.groupby('Period').sum()['Sales_Value']
        return sales_performance.to_dict()
    
    def sales_trends_first_quarter(self):
        first_quarter_data = self.data[self.data['Period'].dt.month.isin([1, 2, 3])]
        sales_trends = first_quarter_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def sales_in_january(self):
        january_data = self.data[self.data['Period'].dt.month == 1]
        sales_trends = january_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def weekly_sales_trends(self):
        self.data['Week'] = self.data['Period'].dt.to_period('W')
        weekly_trends = self.data.groupby('Week').sum()['Sales_Value']
        return weekly_trends.to_dict()
    
    def compare_sales_trends(self, product_a, product_b):
        product_a_data = self.data[self.data['Item Name'] == product_a]
        product_b_data = self.data[self.data['Item Name'] == product_b]
        sales_trends_a = product_a_data.groupby('Period').sum()['Sales_Value']
        sales_trends_b = product_b_data.groupby('Period').sum()['Sales_Value']
        return {'Product A': sales_trends_a.to_dict(), 'Product B': sales_trends_b.to_dict()}
    
    def compare_sales_this_year_last_year(self, product_name):
        this_year = datetime.now().year
        last_year = this_year - 1
        this_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'].dt.year == this_year)]
        last_year_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'].dt.year == last_year)]
        sales_trends_this_year = this_year_data.groupby('Period').sum()['Sales_Value']
        sales_trends_last_year = last_year_data.groupby('Period').sum()['Sales_Value']
        return {'This Year': sales_trends_this_year.to_dict(), 'Last Year': sales_trends_last_year.to_dict()}
    
    def compare_product_to_overall(self, product_name):
        product_data = self.data[self.data['Item Name'] == product_name]
        overall_data = self.data.groupby('Period').sum()['Sales_Value']
        product_sales_trends = product_data.groupby('Period').sum()['Sales_Value']
        return {'Product': product_sales_trends.to_dict(), 'Overall': overall_data.to_dict()}
    
    def sales_in_region(self, region):
        region_data = self.data[self.data['Region'] == region]
        sales_trends = region_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def sales_trends_past_year_region(self, region):
        one_year_ago = datetime.now() - timedelta(days=365)
        region_data = self.data[(self.data['Region'] == region) & (self.data['Period'] >= one_year_ago)]
        sales_trends = region_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def product_sales_in_city_region(self, product_name, region):
        region_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Region'] == region)]
        sales_trends = region_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def monthly_sales_in_region(self, region):
        region_data = self.data[self.data['Region'] == region]
        region_data['Month'] = region_data['Period'].dt.to_period('M')
        sales_trends = region_data.groupby('Month').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def seasonal_sales_trends(self):
        self.data['Season'] = self.data['Period'].dt.month % 12 // 3 + 1
        seasonal_trends = self.data.groupby('Season').sum()['Sales_Value']
        return seasonal_trends.to_dict()
    
    def sales_trends_by_season(self):
        self.data['Season'] = self.data['Period'].dt.month % 12 // 3 + 1
        seasonal_trends = self.data.groupby('Season').sum()['Sales_Value']
        return seasonal_trends.to_dict()
    
    def product_sales_during_summer(self, product_name):
        summer_data = self.data[(self.data['Item Name'] == product_name) & (self.data['Period'].dt.month.isin([6, 7, 8]))]
        sales_trends = summer_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def sales_second_quarter(self):
        second_quarter_data = self.data[self.data['Period'].dt.month.isin([4, 5, 6])]
        sales_trends = second_quarter_data.groupby('Period').sum()['Sales_Value']
        return sales_trends.to_dict()
    
    def compare_sales_second_quarter(self):
        this_year = datetime.now().year
        last_year = this_year - 1
        this_year_second_quarter = self.data[(self.data['Period'].dt.year == this_year) & (self.data['Period'].dt.month.isin([4, 5, 6]))]
        last_year_second_quarter = self.data[(self.data['Period'].dt.year == last_year) & (self.data['Period'].dt.month.isin([4, 5, 6]))]
        sales_trends_this_year = this_year_second_quarter.groupby('Period').sum()['Sales_Value']
        sales_trends_last_year = last_year_second_quarter.groupby('Period').sum()['Sales_Value']
        return {'This Year': sales_trends_this_year.to_dict(), 'Last Year': sales_trends_last_year.to_dict()}