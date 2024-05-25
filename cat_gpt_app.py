import streamlit as st
import openai
from openai import AsyncOpenAI

# Set up the async OpenAI client
client = AsyncOpenAI(api_key=st.secrets["API_key"])

# Function to generate feedback for user inputs using OpenAI's API
async def generate_feedback(prompt, context):
    model = "gpt-3.5-turbo"
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main application function
async def app():
    
    # Display title and image
    st.title("CatGPT: AI Powered Cat Health Assistant")
    st.image("CatGPT.png")
    
    # Introduction text
    st.write(
        """
       Meow! I'm here to help you keep your cat healthy and happy. From nutrition tips to behavior advice, I've got you covered. Ask me anything about your feline friend, and let's make sure they're living their best life together! 🌟
        """
    )
    
    st.write("""Submitted By Allana Yzabelle M. Diaz of BSCS 3A as her Final Project for CCS 229 (Intelligent Systems)""")

    # System context for feedback generation
    system_context = "You are a helpful assistant, only catering to health related concerns of cats. Any concerns unrelated are not your task. Use emojis if possible."

    # Multi-level prompting: Step 1
    what = st.text_input("What is your cat's health concern?")
    if what:
        feedback = await generate_feedback(f"{what} is my cat's health concern. Please acknowledge positively and only ask to provide additional information. Don't ask when, where or why it happened. ", system_context)
        st.write(feedback)
            
        # Multi-level prompting: Step 2
        addtl = st.text_input("Provide any additional information.")
        if addtl:
            feedback = await generate_feedback(f"{addtl} is any additional information towards the concern. Please acknowledge positively. Ask a when question.", system_context)
            st.write(feedback)


            # Multi-level prompting: Step 3
            when = st.text_input("When did you first notice this behavior?")
            if when:
                feedback = await generate_feedback(f"{when} is when it started happening. Please acknowledge positively. Ask a why question.", system_context)
                st.write(feedback)

                # Multi-level prompting: Step 4
                why = st.text_area("Why do you think it started happening?")
                if why:
                    feedback = await generate_feedback(f"{why} is why it started happening. Please acknowledge positively. Ask where the cat is feeling the health concern.", system_context)
                    st.write(feedback)

                    # Multi-level prompting: Step 5
                    where = st.text_input("Where is your cat feeling the health concern?")
                    if where:
                        feedback = await generate_feedback(f"{where} is where the cat feels the health concern. Please acknowledge positively and tell the user to press the button below to provide advice.", system_context)
                        st.write(feedback)

                        
                     # Context for AI generation based on the user's input
                    context = (f"Generate helpful advice or assistance on: what had happened to the cat: {what}, additional information to the concern: {addtl}, when it happened: {when}, "
                            f"why it happened: {why}, where it happened: {where} "
                            f"Please be nice and help the user, include emojis and put it in bullet forms if possible.")
                    question = "What should I do to help my cat?"

                    # Button to generate response
                    if st.button("Get Help from CatGPT"):
                        if question and context:
                           # Generate advice suggestion
                            response = await generate_response(question, context)
                            st.write("CatGPT's Advice")
                            st.write("Important Disclaimer: I am a language model AI and cannot provide medical advice. The information provided is for educational purposes only and should not replace consultation with a qualified veterinarian.")
                            st.write(response)

                        else:
                            st.error("Please make sure you don't leave any field blank.")

# Function to generate the advice response
async def generate_response(question, context):
    model = "gpt-3.5-turbo"
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content

# Run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())