import streamlit as st
import requests

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "2b88ac20-106a-4106-b62a-68c5ca71d4ac"
APPLICATION_TOKEN = "AstraCS:gGySHmNbFXhtZqXhQlUsaEIL:0932b0601e58ec33a02e15f01c4b1109f46fa60e597954009835e5c393911dfd"
ENDPOINT = "ba956d3e-05a2-427c-b1c0-72495d00fd45?stream=false"

def run_flow(message: str) -> dict:
    """
    Call the LangFlow API to process the message.
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Streamlit Interface
st.set_page_config(page_title="Hackonauts Chatbot", layout="centered")

st.title("Chat with Hackonauts")
st.markdown("Data-Driven Social Insights with Langflow and DataStax Astra DB.")

# Input container
with st.container():
    name = st.text_input("Name:", placeholder="Enter your name")
    dob = st.date_input("Date of Birth:")
    time = st.time_input("Time:")
    gender = st.selectbox("Gender:", ["Select", "Male", "Female", "Other"])
    state = st.text_input("State:", placeholder="Enter your state")
    city = st.text_input("City:", placeholder="Enter your city")
    
    # Create user message by concatenating input values
    user_message = f"{name} {dob} {time} {gender} {state} {city} generate horoscope."

# Button and response container
if st.button("Send"):
    if not user_message.strip():
        st.error("⚠ Please enter a valid message.")
    else:
        with st.spinner("Waiting for response..."):
            try:
                # Call LangFlow API with the user message
                response = run_flow(user_message)
                
                # Extract the result
                result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get(
                    "results", {}).get("message", {}).get("text", "No response.")
                
                # Display the result
                st.success("Response Received:")
                st.markdown(f"""
                    <div style="background-color:#f9f9f9; padding:10px; border-radius:5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                        <p style="color:#333; font-size:16px; font-family:Arial, sans-serif;">{result}</p>
                    </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                st.error(f"⚠ An error occurred: {e}")
            except Exception as e:
                st.error(f"⚠ Unexpected error: {e}")
