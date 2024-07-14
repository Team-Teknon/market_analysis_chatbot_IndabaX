import vertexai.preview
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    ResponseValidationError,
    FunctionDeclaration,
    Tool,
)
from tools.product_sales_trends import ProductSalesTrends
from tools.sales_performance_comparison import SalesPerformanceComparison
from tools.market_view import MarketView
from setup import *


df = load_data()  # load data
vertexai.init(project="farmnets-try")


# Create instances of each class
trends = ProductSalesTrends(df.copy())
comparison = SalesPerformanceComparison(df.copy())
market = MarketView(df.copy())


# Function to Get Sales Over Time
def get_sales_over_time(parameters):
    product_name = parameters['product_names']
    city = parameters['city']
    result, note = trends.sales_over_time(transform_data(product_name), transform_data(city))

    if result is not None:
        for product_name, sales_trend in result.items():
            result[product_name] = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v
                                    for k, v in sales_trend.items()}
        return {"sales_over_time": result, "important note": note}
    else:
        return {"error": "No data available"}


def average_unit_price_over_time(parameters):
    product_name = parameters['product_name']
    result = trends.average_unit_price_over_time(transform_data(product_name))

    if result is not None:
        result = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in result.items()}
        return {"average_unit_price_over_time": result}
    else:
        return {"error": "No data available"}


# Function to Compare Sales Value Between Cities
def compare_sales_value(parameters):
    cities = parameters['cities']
    result = comparison.compare_sales_value(transform_data(cities))
    if result is not None:
        # Convert Timestamp keys to string format
        converted_result = {}
        for period, cities_dict in result.items():
            str_period = period.strftime('%Y-%m-%d %H:%M:%S') if isinstance(period, pd.Timestamp) else period
            converted_result[str_period] = cities_dict
        # print(converted_result)
        return {"comparison": converted_result}
    else:
        return {"error": "No data available"}


def compare_average_unit_price(parameters):
    cities = parameters['cities']
    result = comparison.compare_average_unit_price(transform_data(cities))
    if result is not None:
        # Convert Timestamp keys to string format
        converted_result = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in
                            result.items()}
        # print(converted_result)
        return {"comparison": converted_result}
    else:
        return {"error": "No data available"}


def overall_sales_summary(parameters):
    product_name = parameters['product_name']
    try:
        overall_summary = market.overall_sales_summary(transform_data(product_name))
        # Convert Timestamps to strings
        overall_summary_converted = {}
        for metric, values in overall_summary.items():
            overall_summary_converted[metric] = {
                k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in values.items()}

        # print(overall_summary_converted)
        return {"overall_sales_summary": overall_summary_converted}
    except Exception as e:
        return {"error": str(e)}


def top_performing_products(parameters):
    number = parameters['top_n']
    result = market.top_performing_products(top_n=int(number))
    if result is not None:
        return {"top_performing_products": result}
    else:
        return {"error": "No data available"}


# Tools
tools = Tool(function_declarations=[
    FunctionDeclaration(
        name="get_sales_over_time",
        description="Get sales over time for specific products, all products, or randomly selected products in a city "
                    "or all cities",
        parameters={
            "type": "object",
            "properties": {
                "product_names": {
                    "type": "array",
                    "description": "A list containing either one of the following: 'All products' to get sales for "
                                   "all products, or 'Some products' to get sales for randomly selected products; or "
                                   "is an array of product names."
,
                    "default": ["All products"],
                },
                "city": {
                    "type": "string",
                    "description": "The name of a single city, or 'All cities' to get sales in all "
                                   "cities",
                    "default": "All cities",
                }
            },
            "required": ["product_names", "city"]
        }
    ),
    FunctionDeclaration(
        name="average_unit_price_over_time",
        description="Get average unit price over time for a specific product",
        parameters={
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "specifies the specific product name or all products where relevant"
                }
            }
        },
    ),
    FunctionDeclaration(
        name="compare_average_unit_price",
        description="Compare unit prices between two cities",
        parameters={
            "type": "object",
            "properties": {
                "cities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of cities to compare"
                }
            }
        },
    ),
    FunctionDeclaration(
        name="compare_sales_value",
        description="Compare sales value between two cities",
        parameters={
            "type": "object",
            "properties": {
                "cities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of cities to compare"
                }
            }
        },
    ),
    FunctionDeclaration(
        name="overall_sales_summary",
        description="Get overall sales summary over time",
        parameters={
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Product name"
                }
            }
        },
    ),
    FunctionDeclaration(
        name="top_performing_products",
        description="Get top performing products based on sales",
        parameters={
            "type": "object",
            "properties": {
                "top_n": {
                    "type": "integer",
                    "description": "Number of top performing products to return"
                }
            }
        },
    ),
])

# Dispatch table for function handling
function_handlers = {
    "compare_sales_value": compare_sales_value,
    "compare_average_unit_price": compare_average_unit_price,
    "average_unit_price_over_time": average_unit_price_over_time,
    "get_sales_over_time": get_sales_over_time,
    "overall_sales_summary": overall_sales_summary,
    "top_performing_products": top_performing_products,
}
