import yfinance as yf
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)

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

# Model Initialization
model = GenerativeModel("gemini-pro",
                        generation_config={"temperature": 0},

                        tools=[tools])
chat = model.start_chat()

# Send a prompt to the chat
prompt = "What is the stock price of Apple?"
response = chat.send_message(prompt)

# Check for function call and dispatch accordingly
function_call = response.candidates[0].content.parts[0].function_call

# Dispatch table for function handling
function_handlers = {
    "get_stock_price": get_stock_price,
}

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
        print("Chat Response:", chat_response)
    else:
        print("No arguments found for the function.")
else:
    print("Chat Response:", response.text)