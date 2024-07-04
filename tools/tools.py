#import numpy as np
import pandas as pd
from product_sales_trends import ProductSalesTrends
from sales_performance_comparison import SalesPerformanceComparison
from market_view import MarketView

# Load the dataset
df = pd.read_excel('../data/dummy_dataset.xlsx', sheet_name='Database')

# Create instances of each class
trends = ProductSalesTrends(df)
comparison = SalesPerformanceComparison(df)
market = MarketView(df)

#print(df["Item Name"].unique())
#print(df["City"].unique())

alyssa_result = trends.sales_over_time('ALYSSA  SPAGHETTI    200G SACHET')
print("Sales over time for ALYSSA SPAGHETTI: {}".format(alyssa_result))


compare_result = comparison.compare_sales_value(['Abidjan', 'Bouake'])
#print("Comparison of sales value: {}".format(compare_result))