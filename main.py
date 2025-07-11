a = 'sk-proj'
b = '-oR5sgSN3FyqBbEgnzYp5dT6TVPH0yiJj5bDd81DzwxL2NrNB9weRiU4Dqkdy3'
c = 'Y20IEyJUgwn5PT3BlbkFJoBUjM0Z4ri0azrKQ696NWCDypjdDIzZTDClJ'
d = '-kwEBWjVlv5XLEnjZ8GV-LN5EuvKkJIBp612kA'
OPENAI_API_KEY = a+b+c+d

import os
import streamlit as st
import asyncio


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ✅ Agent SDK imports
from openai.agents import Agent, FileSearchTool, Runner

# ✅ Define your agent
agent = Agent(
    name="Assistant",
    instructions="""
You are a Political Thought Expert Agent trained on the book "Political Thought from Plato to the Present" by M. Judd Harmon.

Your role is to accurately answer user questions using only the information available in the book. You must ground all your responses in the retrieved passages and reflect the author’s interpretations, historical context, and original arguments.

Guidelines:
- Cite relevant sections or philosophers when appropriate.
- If multiple interpretations exist (e.g., between Hobbes and Locke), present both sides based on the book’s content.
- Do not invent information or speculate beyond what is in the text.
- If the answer is not found in the book, respond: “The book does not provide a specific answer to this question.”
- Prioritize clarity, academic tone, and fidelity to the author’s language and philosophy.
- You are allowed to quote or paraphrase directly from the text to support your answer.
- If you don't find the answer, then try again with a different approach.
""",
    model='gpt-4o-mini',
    tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_6870917e789c81918db7d50d7cdcd5a7"],
        ),
    ],
)

# ✅ Async wrapper
async def run_agent(input_text):
    return await Runner.run(agent, input=input_text)

# ✅ Streamlit UI
st.set_page_config(page_title="📘 Political Chatbot")
st.title("Political Chatbot 📘")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []
# Chat history loop — show past messages ONLY
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input (new message)
user_input = st.chat_input("Ask your question here...")
if user_input:
    # Run assistant
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = asyncio.run(run_agent(user_input))
            response = result.final_output
            st.markdown(response)

    # Store both messages only ONCE
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("assistant", response))
