# import numpy as np
import pandas as pd
from product_sales_trends import ProductSalesTrends
from sales_performance_comparison import SalesPerformanceComparison
from market_view import MarketView

# Load the dataset
df = pd.read_excel('../data/dummy_dataset.xlsx', sheet_name='Database')
# print(df.describe())

# Create instances of each class
trends = ProductSalesTrends(df.copy())
comparison = SalesPerformanceComparison(df.copy())
market = MarketView(df.copy())

# print(df["Item Name"].unique())
# print(df["City"].unique())

# Example Query: Sales over time for a specific produce
# alyssa_result = trends.sales_over_time('ALYSSA  SPAGHETTI    200G SACHET')
# print("Sales over time for ALYSSA SPAGHETTI: {}".format(alyssa_result))

# Example Query: Comparison of sales value between two cities
# compare_result = comparison.compare_sales_value(['Abidjan', 'Bouake'])
# print("Comparison of sales value: {}".format(compare_result))

# overall_sales_summary = market.overall_sales_summary('ALYSSA  SPAGHETTI    200G SACHET')
# print(overall_sales_summary)

vol_time = trends.sales_volume_over_time('ALYSSA  SPAGHETTI    200G SACHET')
print(vol_time)