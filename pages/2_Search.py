from utils import myFunc as my
from utils import llm_dict
from dotenv import load_dotenv

import os, json, time, requests
from datetime import datetime
import streamlit as st
import altair as alt

from openai import OpenAI # for perplexity
from tavily import TavilyClient
from langchain.adapters.openai import convert_openai_messages
from langchain_community.chat_models import ChatOpenAI

# Introduction

def main():
    
    st.set_page_config(
        page_title = "Search",
        page_icon = "",
        layout="wide",
        initial_sidebar_state="expanded")

    st.header("Web Search 사용")

    # side
    st.sidebar.title("Search Agents")
    my.sidebar_sublist() # sidebar sub list

    st.sidebar.markdown("---") # section 1

    LLM_LIST = ['Perplexity','Open AI'] # 변경 필요
    
    _llm_to_use = st.sidebar.selectbox('선택할 LLM', LLM_LIST)

    # model selection
    LLM_MODEL = llm_dict.LLM_DICT[_llm_to_use]['MODEL']
    _model_to_use = st.sidebar.selectbox('선택할 모델', LLM_MODEL)

    # API connection
    API_KEY = llm_dict.LLM_DICT[_llm_to_use]['API']
    _api_to_use = my.api_key_loader(API_KEY)
    
    st.sidebar.markdown("---") # section 2

    # MAIN PAGE
    col1, col2, col3 = st.columns([1,2,1])  # section separated

    # Chat Agent

    if _llm_to_use == LLM_LIST[0]: # if perplexity selected
        
        client = OpenAI(api_key = _api_to_use, 
                        base_url="https://api.perplexity.ai")
    
        with col1:
            st.write("TO BE UPDATED: PARAMETERS")
            # Store the initial value of widgets in session state
            if "visibility" not in st.session_state:
                st.session_state.visibility = "visible"
                st.session_state.disabled = False
     
            st.checkbox("Open AI System 값 고정", key="disabled")
            st.radio(
                "Set text input label visibility 👉",
                key="visibility", # key
                options=["visible", "hidden", "collapsed"],
            )
        
            system_request = st.text_input(
                "Enter System Requests to Open AI 👇",
                label_visibility=st.session_state.visibility, # st.radio 선택 옵션에 따라 결정
                disabled=st.session_state.disabled, # visibility 옵션 선택시, visible 아니면 false
                # placeholder=st.session_state.placeholder, # 입력 값
            )
        
            if system_request:
                st.write("System Role: ", system_request) # 최종 받아오는 input

            prompt_request = st.text_input(
                "Enter Prompt to Open AI 👇")
        
            if prompt_request:
                st.write("Your prompt: ", prompt_request) # 최종 받아오는 input

        
        with col2:

            if "plx_search" not in st.session_state:
                st.session_state["plx_search"] = [
                    {"role" : "system",
                     "content" : "무엇을 검색하시겠습니까?"}
                ]

            if "search_history" not in st.session_state:
                st.session_state["search_history"] = [] # store full search history

            
            if st.sidebar.button("clear conversation history"):
                st.session_state["plx_search"] = [
                    {"role" : "system",
                     "content": "무엇을 검색하시겠습니까?"}
                ]
                st.sidebar.success("Conversation history cleared!")
    
            if st.sidebar.button("clear search history"):
                st.session_state["Search_history"] = []
                st.sidebar.success("Search history cleared!")

            for msg in st.session_state["plx_search"]:
                with st.chat_message(msg["role"]): # assistant
                    st.markdown(msg["content"]) # 무엇을 검색하시겠습니까
            
            # Process new user input
            if prompt := st.chat_input(placeholder="원하는 질문을 입력해주세요"):
                # Add user message to the session
                st.session_state.plx_search.append({"role": "user",
                                                    "content": prompt})
                
                with st.chat_message("user"): # 나의
                    st.markdown(prompt) # 입력내용
            
                try:
                    valid_messages = [
                        {'role': msg['role'],
                         'content': msg['content']}
                        for msg in st.session_state['plx_search']
                        if msg['role'] in ['user', 'assistant']
                    ]
    
                    stream = client.chat.completions.create(
                        model=_model_to_use,
                        messages = valid_messages,
                        stream = True
                    )
                    response = st.write_stream(stream)
        
                    st.session_state.plx_search.append(
                        {"role": "assistant", "content": response}
                    )
    
                    st.session_state["search_history"].append(
                        {'query': prompt,
                        'response': response}
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
        with col3:
            st.write("### Search history")
            for entry in st.session_state['search_history']:
                st.write(f"-**QUERY**: {entry['query']}")
                st.write(f"-**RESPONSE**: {entry['response']}")
                
    elif _llm_to_use == LLM_LIST[1] : # if open ai selected, mixing with tavily API
        
        with col1:
            st.write("TO BE UPDATED: PARAMETERS")
            # Store the initial value of widgets in session state
            if "visibility" not in st.session_state:
                st.session_state.visibility = "visible"
                st.session_state.disabled = False
     
            st.checkbox("Open AI System 값 고정", key="disabled")
            st.radio(
                "Set text input label visibility 👉",
                key="visibility", # key
                options=["visible", "hidden", "collapsed"],
            )
        
            system_request = st.text_input(
                "Enter System Requests to Open AI 👇",
                label_visibility=st.session_state.visibility, # st.radio 선택 옵션에 따라 결정
                disabled=st.session_state.disabled, # visibility 옵션 선택시, visible 아니면 false
                # placeholder=st.session_state.placeholder, # 입력 값
            )
        
            if system_request:
                st.write("System Role: ", system_request) # 최종 받아오는 input

            prompt_request = st.text_input(
                "Enter Prompt to Open AI 👇")
        
            if prompt_request:
                st.write("Your prompt: ", prompt_request) # 최종 받아오는 input

        with col2:

            if "search_history" not in st.session_state:
                st.session_state['search_history']=[]

            if "tavily_search" not in st.session_state:
                st.session_state['tavily_search'] = [
                    {'depth': 'advanced',
                     'content': "무엇을 검색하시겠습니까?"}
                ]

            if st.sidebar.button("clear Chat history"):
                st.session_state['tavily_search']=[
                    {'depth': 'advanced',
                     'content': "무엇을 검색하시겠습니까?"}
                ]
                st.sidebar.success("Search Chat cleared!")

            if st.sidebar.button("clear Search history"):
                st.session_state['search_history']=[]
                st.sidebar.success("Search history cleared!")

            # st.write("### Conversation history")

            for msg in st.session_state["tavily_search"]:
                with st.chat_message(msg["depth"]): # icon 이미지
                    st.markdown(msg["content"]) # 무엇을 검색하시겠습니까

            if prompt := st.chat_input(placeholder="원하는 질문을 입력해주세요"):

                st.session_state["tavily_search"].append({"depth": "advanced",
                                                          "content": prompt})

                try:
                    tavilyAPI = my.api_key_loader(llm_dict.LLM_DICT['Tavily']['API'],
                                                  save_path=SAVE_PATH)
                    
                    tavilyClient = TavilyClient(api_key = tavilyAPI)
                    
                    tavily_answer = tavilyClient.search(prompt,
                                                        search_depth='advanced')["results"]
                    openai_prompt = [
                        {
                            "role": "system",
                            "content": f"{system_request}"
                        },
                        
                        {
                            "role" : "user",
                            "content": 
                            f"""
                            Information: {tavily_answer}
                            Requests: {prompt_request}
                            """
                        }
                    ]
    
                    lc_messages = convert_openai_messages(openai_prompt)
                    
                    report = ChatOpenAI(model = _model_to_use,
                                        openai_api_key = _api_to_use).invoke(lc_messages).content


                    st.markdown(report)
    
                    st.session_state["search_history"].append(
                        {'query': prompt,
                        'response': report}
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
        with col3:
                
            st.write("### Search history")
            for entry in st.session_state['search_history']:
                st.write(f"-**QUERY**: {entry['query']}")
                st.write(f"-**RESPONSE**: {entry['response']}")


    else:
        st.write("error in llm selection")

if __name__ == "__main__" :
    main()
