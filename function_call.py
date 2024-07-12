import time

import pandas as pd
from tools.product_sales_trends import ProductSalesTrends
from tools.sales_performance_comparison import SalesPerformanceComparison
from tools.market_view import MarketView
from vertexai.generative_models import ResponseValidationError
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from setup import *

df = load_data()  # load data

# Create instances of each class
trends = ProductSalesTrends(df.copy())
comparison = SalesPerformanceComparison(df.copy())
market = MarketView(df.copy())


# Function to Get Sales Over Time
def get_sales_over_time(parameters):
    product_name = parameters['product_name']
    result = trends.sales_over_time(transform_data(product_name))
    # print("Transformed product name:", transform_data(product_name))
    # print(result)

    if result is not None:
        result = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in result.items()}
        # print(result)
        return {"sales_over_time": result}
    else:
        return {"error": "No data available"}


# Function to Get Sales Volume Over Time
def sales_volume_over_time(parameters):
    product_name = parameters['product_name']
    result = trends.sales_volume_over_time(transform_data(product_name))
    # print(result)
    # print("Product name: ", product_name)
    if result is not None:
        # Convert Timestamp keys to string format
        result = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in result.items()}
        # print(result)
        return {"sales_volume_over_time": result}
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
    

def overall_sales_summary(parameters):
    product_name = parameters['product_name']
    try:
        overall_summary = market.overall_sales_summary(transform_data(product_name))
        # Convert Timestamps to strings
        overall_summary_converted = {}
        for metric, values in overall_summary.items():
            overall_summary_converted[metric] = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in values.items()}

        # print(overall_summary_converted)
        return {"overall_sales_summary": overall_summary_converted}
    except Exception as e:
        return {"error": str(e)}


# Tools
tools = Tool(function_declarations=[
    FunctionDeclaration(
        name="get_sales_over_time",
        description="Get sales over time for a specific product",
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
        name="sales_volume_over_time",
        description="Get sales volume over time for a specific product",
        parameters={
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Product name"
                }
            }
        }
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
    )
])

# Dispatch table for function handling
function_handlers = {
    "compare_sales_value": compare_sales_value,
    "get_sales_over_time": get_sales_over_time,
    "sales_volume_over_time": sales_volume_over_time,
    "overall_sales_summary": overall_sales_summary,
}

# Model Initialization
model = GenerativeModel("gemini-pro",
                        generation_config={"temperature": 0},
                        tools=[tools])
chat = model.start_chat()


def chat_gemini(prompt):
    # Send a prompt to the chat
    try:
        response = chat.send_message(prompt)  # send user prompt to Gemini and receive response

        # Check for function call and dispatch accordingly
        function_call = response.candidates[0].content.parts[0].function_call

        print(function_call)

        if function_call.name in function_handlers:
            function_name = function_call.name

            args = {key: value for key, value in function_call.args.items()}

            # Call the function with the extracted arguments
            if args:
                function_response = function_handlers[function_name](args)

                # Sending the function response back to the chat
                response = chat.send_message(
                    Part.from_function_response(
                        name=function_name,
                        response={
                            "content": function_response,
                        }
                    ),
                )

                print(response)

                chat_response = response.candidates[0].content.parts[0].text
                return True, chat_response
                # print("Chat Response:", chat_response)
            else:
                print("No arguments found for the function.")
        else:
            return True, response.text
    except ResponseValidationError:
        return False, "Sorry, the response wasn't valid. Please try again"
    except AttributeError as e:
        return False, f"AttributeError occurred: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"
