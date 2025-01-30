from utils import myFunc as my
from utils import llm_dict

import os, json, time, requests
import streamlit as st

# Introduction

def main():

    st.set_page_config(
        page_title = "RAG",
        page_icon = "",
        layout="wide",
        initial_sidebar_state="expanded")

    # message
    # st.title(); st.header()
    
    # side
    st.sidebar.title("RAG Agents")

    with st.sidebar:
            
        st.sidebar.page_link("main.py", label="Main Page", icon=":material/home:")
    
        st.subheader("LLM Subpages")
        st.page_link("pages/1_Chat.py", label="chat page", icon=":material/chat:")
        st.page_link("pages/2_Search.py", label="Search", icon=":material/search:")
        st.page_link("pages/3_RAG.py", label="RAG", icon=":material/content_copy:")
        st.page_link("pages/4_Creation.py", label="Creation", icon=":material/animated_images:")

        st.subheader("My Portfolio Page")
        st.page_link(
            page="https://www.notion.so/6a3376726c024eaca041dbcc8ab077b5",
            label="**Notion Page**",
            icon=":material/apps:",
        )
        
    st.sidebar.markdown("---")


    # st.sidebar.subheader("")

    # Sidebar (소스코드 루트에서 toml 작업 통해 기본 사이드바를 숨길 수 있음)
    # reference: https://jjnomad.tistory.com/53)
    
    # st.sidebar.page_link("home.py", label="Home")
    # st.sidebar.page_link("pages/1_edit.py", label="Edit Page")
    # st.sidebar.page_link("pages/2_reference.py", label="Reference")
    
    st.sidebar.markdown("---")

    # API KEY
    
    # Agent ID


if __name__ == "__main__" :
    main()

# end of code
