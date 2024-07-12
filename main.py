import streamlit as st
from function_call import *

# Model Initialization
model = GenerativeModel("gemini-pro",
                        generation_config={"temperature": 0},
                        tools=[tools])
chat = model.start_chat()

chat.send_message(
    "You are a knowledgeable and helpful AI assistant named IndaBot. Your expertise lies in market performance analysis"
    " and data interpretation. You will provide users with insights, trends, and answers to their questions about "
    "market data, helping them understand and act on the information effectively."
)


def chat_gemini(prompt):
    # Send a prompt to the chat
    try:
        gemini_response = chat.send_message(prompt)  # send user prompt to Gemini and receive response

        # Check for function call and dispatch accordingly
        function_call = gemini_response.candidates[0].content.parts[0].function_call

        print(function_call)

        if function_call.name in function_handlers:
            function_name = function_call.name

            args = {key: value for key, value in function_call.args.items()}

            # Call the function with the extracted arguments
            # if args:
            function_response = function_handlers[function_name](args)

            # Sending the function response back to the chat
            gemini_response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={
                        "content": function_response,
                    }
                ),
            )

            chat_response = gemini_response.candidates[0].content.parts[0].text
            return True, chat_response
            # else:
            #     return True, "No arguments found for the function."
        else:
            return True, gemini_response.text
    except ResponseValidationError:
        return False, "Sorry, the response wasn't valid. Please try again"
    except AttributeError as e:
        print("Error message: ", str(e))
        return False, f"AttributeError occurred. Please check the logs and try again."
    except Exception as e:
        print("Error message: ", str(e))
        return False, f"An unexpected error occurred. Please check the logs and try again."


# Bot title
st.title("IndabaX Bot")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
user_prompt = st.chat_input("Type your message here")
if user_prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    success, response = chat_gemini(user_prompt)
    response = (f"IndaBot:  "
                f"{response}")
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    if not success:
        print(f"There was an error:{response}")
