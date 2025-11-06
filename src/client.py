import requests
import streamlit as st

st.title("FastAPI ChatBot")

if "messages" not in st.session_state:
	st.session_state.messages = []


for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

prompt = st.text_area("Prompt or URL (e.g., Wikipedia link)", height=150)
model = st.selectbox("Model", ["TinyLlama/TinyLlama-1.1B-Chat-v1.0"])
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

if st.button("Generate Text"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                response = requests.post(
                    "http://localhost:8000/generate/text",
                    json={
                        "prompt": prompt,
                        "model": model,
                        "temperature": temperature
                    }
                )
                response.raise_for_status()
                data = response.json()
                st.subheader("Generated Text")
                st.markdown(data.get("content", "No content received."))

            except requests.exceptions.RequestException as e:
                st.error(f"Error contacting FastAPI: {e}")