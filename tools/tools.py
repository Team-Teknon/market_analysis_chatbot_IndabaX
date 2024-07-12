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
"""
['ALYSSA  SPAGHETTI    200G SACHET'
 'MAMAN     SUPERIOR QUALITY FOOD PASTA 200G SACHET'
 'MAMAN  VERMICELLI    200G SACHET' 'MAMAN 1.1 SPAGHETTI    200G SACHET'
 'MAMAN 1.5 SPAGHETTI    200G SACHET' "BLE D'OR      200G SACHET"
 'MAMAN  SPAGHETTI    200G SACHET' 'MAMAN 1.5 SPAGHETTI    500G SACHET'
 'MONDO  SPAGHETTI    500G SACHET' 'MAMAN  SPAGHETTI    4540G BAG'
 'MAMAN  COQUILLETTES    200G SACHET' 'DOUBA      500G SACHET'
 'PAGANINI  SPAGHETTI    200G SACHET' 'PANZANI  CAPELLINI    500G SACHET'
 'PANZANI  TORTI  WITH TOMATO & SPINACH  500G BAG'
 'PASTA DOUBA  SPAGHETTI    500G SACHET'
 "BLE D'OR  SPAGHETTI    200G SACHET" 'PASTA AROMA      200G SACHET'
 'MAMAN  COQUILLETTES    4540G BAG'
 'MAMAN  VERMICELLI   SUPERIOR QUALITY FOOD PASTA 4540G BAG'
 'MAMAN  SPAGHETTI    500G SACHET' 'MAMAN  VERMICELLI    500G SACHET'
 'BONJOURNE  SPAGHETTI    500G SACHET' 'MAMAN  SPAGHETTI    475G SACHET'
 'PANZANI GOLD SPAGHETTI   QUALITY 250G SACHET'
 'MAMAN  MACARONI    200G SACHET' 'MAMAN  SPAGHETTI    450G SACHET'
 'TAT MAKARNA  SPAGHETTI    500G SACHET'
 'PASTA MONDO  SPAGHETTI    200G SACHET' 'REINE  PASTA    500G SACHET'
 'PASTA BOUBA      500G SACHET' 'BONJOURNE  SPAGHETTI    200G SACHET'
 'MAMAN      200G SACHET' 'GOUSTA  SPAGHETTI   ALTA QUALITA 200G SACHET'
 'PANZANI  SPAGHETTI    500G SACHET'
 'OBA MAKARNA  SPAGHETTI    200G SACHET']
"""
# print(df["City"].unique())
"""
['Abidjan' 'Bouake']
"""

# Example Query: Sales over time for a specific produce
# alyssa_result = trends.sales_over_time('ALYSSA  SPAGHETTI    200G SACHET')
# print("Sales over time for ALYSSA SPAGHETTI: {}".format(alyssa_result))

# Example Query: Comparison of sales value between two cities
# compare_result = comparison.compare_sales_value(['Abidjan', 'Bouake'])
# print("Comparison of sales value: {}".format(compare_result))

# overall_sales_summary = market.overall_sales_summary('ALYSSA  SPAGHETTI    200G SACHET')
# print(overall_sales_summary)

# vol_time = trends.sales_volume_over_time('ALYSSA  SPAGHETTI    200G SACHET')
# print(vol_time)

# avg_unit_price = trends.average_unit_price_over_time('ALYSSA  SPAGHETTI    200G SACHET')
# print(avg_unit_price)

# trend_by_period = trends.product_sales_trends("ALYSSA  SPAGHETTI    200G SACHET", "custom_month", month="January")
# print(trend_by_period)

top_perform = market.top_performing_products(top_n=1)
print(top_perform)