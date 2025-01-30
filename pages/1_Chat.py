from utils import myFunc as my
from utils import llm_dict

import os, json, time, requests
from datetime import datetime
import streamlit as st
import altair as alt

from openai import OpenAI
# import asyncio
# from openai import AsyncOpenAI

# Introduction

def main():

    st.set_page_config(
        page_title = "Basic Chat Playground",
        page_icon = "",
        layout="wide",
        initial_sidebar_state="expanded")

    # message
    st.header("Basic Chat 기능 사용")
    
    st.sidebar.title("Chat Agents")
    my.sidebar_sublist() # sidebar sub list
        
    st.sidebar.markdown("---")

    # LLM OPTIONS
    LLM_LIST = ['Open AI','XAI','Google: Chat']
    _llm_to_use = st.sidebar.selectbox('선택할 LLM', LLM_LIST)

    # model selection
    LLM_MODEL = llm_dict.LLM_DICT[_llm_to_use]['MODEL']
    _model_to_use = st.sidebar.selectbox('선택할 모델', LLM_MODEL)

    # API connection
    API_KEY = llm_dict.LLM_DICT[_llm_to_use]['API']
    _api_to_use = my.api_key_loader(API_KEY)

    st.sidebar.markdown("---")

    # MAIN PAGE

    col1, col2 = st.columns([2,1])  # section separated

    # Open AI Case with stream messages
    if _llm_to_use == LLM_LIST[0]: # Open AI selected

        with col1:
            client = OpenAI(api_key = _api_to_use)

            # Ensure session state exists
            if "messages" not in st.session_state:
                st.session_state["messages"] = [{"role": "assistant",
                                                 "content": "무엇을 도와드릴까요"}]
    
            if "message_history" not in st.session_state:
                st.session_state["message_history"] = []
    
            if st.sidebar.button("clear conversation history"):
                st.session_state["messages"] = [{"role": "assistant",
                                                 "content": "무엇을 도와드릴까요"}]
                st.sidebar.success("Message Chat cleared")
    
            if st.sidebar.button("clear message history"):
                st.session_state["message_history"] = []
                st.sidebar.success("Message History Cleared!")
            
            # Display conversation history
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Process new user input
            if prompt := st.chat_input(placeholder="원하는 질문을 입력해주세요"):
                # Add user message to the session
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
            
                # Call OpenAI API to generate assistant response
                try:
                    # start_time = time.time()
    
                    with st.chat_message("assistant"):
                        stream = client.chat.completions.create(
                            model=_model_to_use,  # Specify the model you want to use
                            messages=[
                                {'role':m['role'], 'content':m['content']}
                                for m in st.session_state.messages
                            ],
                            stream=True
                        )
                        response = st.write_stream(stream)
    
                        st.session_state.messages.append({"role": "assistant", "content": response})
    
                        st.session_state["message_history"].append(
                            {'query': prompt,
                            'response': response}
                        )
                    
                    # print('Response complete: '+f'{time.time()-start_time:.2f} sec')
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")


        with col2:
                
            st.write("### Message history")
            for entry in st.session_state['message_history']:
                st.write(f"-**QUERY**: {entry['query']}")
                st.write(f"-**RESPONSE**: {entry['response']}")

    
    elif _llm_to_use == LLM_LIST[1]: # XAI
        st.write("To be updated")

    elif _llm_to_use == LLM_LIST[2]: # Google
        st.write("To be updated")

    else:
        st.write("None of model is selected")

if __name__ == "__main__" :
    main()

# end of code
