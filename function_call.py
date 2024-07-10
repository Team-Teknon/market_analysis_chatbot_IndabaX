import pandas as pd
from tools.product_sales_trends import ProductSalesTrends
from tools.sales_performance_comparison import SalesPerformanceComparison
from tools.market_view import MarketView
import yfinance as yf
from vertexai.generative_models import ResponseValidationError
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
import time

# Load the dataset
df = pd.read_excel('data/dummy_dataset.xlsx', sheet_name='Database')

# Create instances of each class
trends = ProductSalesTrends(df)
comparison = SalesPerformanceComparison(df)
market = MarketView(df)


# Function to Get Sales Over Time
def get_sales_over_time(parameters):
    product_name = parameters['product_name']
    result = trends.sales_over_time(product_name)
    if result is not None:
        result = {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in result.items()}
        return {"sales_over_time": result}
    else:
        return {"error": "No data available"}


# Function to Compare Sales Value Between Cities
def compare_sales_value(parameters):
    cities = parameters['cities']
    result = comparison.compare_sales_value(cities)
    if result is not None:
        return {"comparison": result}


# Function to Get Stock Price
def get_stock_price(parameters):
    ticker = parameters['ticker']
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if not hist.empty:
        return {"price": hist['Close'].iloc[-1]}
    else:
        return {"error": "No data available"}


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
        name="get_stock_price",
        description="Get the current stock price of a given company",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                }
            }
        },
    )
])

# Dispatch table for function handling
function_handlers = {
    "get_stock_price": get_stock_price,
    "compare_sales_value": compare_sales_value,
    "get_sales_over_time": get_sales_over_time
}

# Model Initialization
model = GenerativeModel("gemini-pro",
                        generation_config={"temperature": 0},
                        tools=[tools])
chat = model.start_chat()


def chat_gemini(prompt):
    # Send a prompt to the chat
    try:
        response = chat.send_message(prompt)

        # Check for function call and dispatch accordingly
        function_call = response.candidates[0].content.parts[0].function_call

        print(function_call)

        if function_call.name in function_handlers:
            function_name = function_call.name

            # Directly extract arguments from function call
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

                chat_response = response.candidates[0].content.parts[0].text
                return True, chat_response
                # print("Chat Response:", chat_response)
            else:
                print("No arguments found for the function.")
        else:
            return True, response.text
            # print("Chat Response:", response.text)
    except ResponseValidationError:
        return False, "Sorry, the response wasn't valid. Please try again"
