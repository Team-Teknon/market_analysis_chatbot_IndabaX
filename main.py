import streamlit as st
import yfinance as yf
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from function_call import *

# Bot title
st.title("IndabaX Bot")


# # Model Initialization
# model = GenerativeModel("gemini-pro",
#                         generation_config={"temperature": 0},
#
#                         tools=[tools])
# chat = model.start_chat()
#
# # Send a prompt to the chat
# prompt = "What is the stock price of Apple?"
# response = chat.send_message(prompt)
#
# # Check for function call and dispatch accordingly
# function_call = response.candidates[0].content.parts[0].function_call
#
# # Dispatch table for function handling
# function_handlers = {
#     "get_stock_price": get_stock_price,
# }
#
# if function_call.name in function_handlers:
#     function_name = function_call.name
#
#     # Directly extract arguments from function call
#     args = {key: value for key, value in function_call.args.items()}
#
#     # Call the function with the extracted arguments
#     if args:
#         function_response = function_handlers[function_name](args)
#
#         # Sending the function response back to the chat
#         response = chat.send_message(
#             Part.from_function_response(
#                 name=function_name,
#                 response={
#                     "content": function_response,
#                 }
#             ),
#         )
#
#         chat_response = response.candidates[0].content.parts[0].text
#         print("Chat Response:", chat_response)
#     else:
#         print("No arguments found for the function.")
# else:
#     print("Chat Response:", response.text)

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Type your message here")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    success, response = chat_gemini(prompt)
    response = (f"IndaBot:  "
                f"{response}")
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    if not success:
        print(f"There was an error:{response}")
