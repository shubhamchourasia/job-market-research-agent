import streamlit as st
import ollama
from duckduckgo_search import DDGS
from datetime import date

# 1. Get real-time date from your Mac
today_str = date.today().strftime("%B %d, %Y")

st.set_page_config(page_title="Local Gemini", layout="centered")

# (Keep your CSS here)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        context = ""
        
        # 2. Force Search for "Real-Time" queries
        with st.status("Thinking...", expanded=False) as status:
            try:
                with DDGS() as ddgs:
                    # We search for the user's prompt to get latest snippets
                    search_results = [r for r in ddgs.text(prompt, max_results=5)]
                    context = "\n".join([f"FACT: {r['body']}" for r in search_results])
                    status.update(label="Web info retrieved!", state="complete")
            except Exception as e:
                status.update(label="Search failed, using local brain.", state="error")

        # 3. The "Gemini" System Prompt
        # This tells the model exactly what day it is and gives it the search data
        messages = [
            {
                'role': 'system', 
                'content': f"Today is {today_str}. Use the following search results to answer precisely: {context}"
            },
            *st.session_state.messages
        ]

        # 4. Stream from Ollama
        stream = ollama.chat(model='qwen2.5:7b', messages=messages, stream=True)

        for chunk in stream:
            full_response += chunk['message']['content']
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})