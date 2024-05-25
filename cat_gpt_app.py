import streamlit as st
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Retrieve the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is loaded
if not api_key:
    st.error("API key is missing. Please set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = api_key

    st.title("CatGPT Health Assistant ฅ^•ﻌ•^ฅ ")

    # Read disclaimer from file
    try:
        with open("disclaimer.txt", "r") as f:
            disclaimer = f.read()
    except FileNotFoundError:
        disclaimer = "Disclaimer not found. Please make sure disclaimer.txt exists."

    user_prompt = st.text_input("Ask me anything about cats!")

    if user_prompt:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{disclaimer} Here's what I found about {user_prompt} in cats:",
            max_tokens=250,  # Adjust for desired response length
            n=1,
            stop=None,
            temperature=0.7,
        )

        st.write(disclaimer)
        st.write(response.choices[0].text.strip())
