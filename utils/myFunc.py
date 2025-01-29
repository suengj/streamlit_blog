from dotenv import load_dotenv
import os, json, time, requests
from datetime import datetime
import streamlit as st

def api_key_loader(API_KEY, save_path=""):

    try:
        load_dotenv(save_path)
        api_key = os.environ.get(API_KEY)

    except:
        api_key = st.secrets['OPENAI_API_KEY']

    return api_key

# sub page link
def sidebar_sublist():
        # side
    with st.sidebar:
            
        st.page_link("main.py", label="Main", icon=":material/home:")
    
        st.subheader("AI: LLM Models")
        st.page_link("pages/1_Chat.py", label="chat page", icon=":material/chat:")
        st.page_link("pages/2_Search.py", label="Search", icon=":material/search:")
        st.page_link("pages/3_RAG.py", label="RAG", icon=":material/content_copy:")
        st.page_link("pages/4_Creation.py", label="Creation", icon=":material/animated_images:")

        st.subheader("Side Projects")
        st.write("맛대리 - 업데이트 예정")

        st.subheader("Others")
        st.page_link(
            page="https://www.linkedin.com/in/suengjaehong/",
            label="**Linkedin**",
             icon=":material/apartment:",
        )
        st.write("**Notion : To-be updated**")
        # st.page_link(
        #     page="",
        #     label="**Notion**",
        #     icon=":material/apps:",
        # )


## NOT USE CURRENTLY
def authenticated_menu():
    None
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("main.py", label="Home")
    # st.sidebar.page_link("./pages/1_Chat.py", label="Basic Chat")
    # st.sidebar.page_link("pages/2_Search.py", label="Search")
    # st.sidebar.page_link("pages/3_RAG.py", label="RAG")
    # st.sidebar.page_link("pages/4_Creation.py", label="Creation")

    # if st.session_state.role in ["admin", "super-admin"]:
    #     st.sidebar.page_link("pages/admin.py", label="Manage users")
    #     st.sidebar.page_link(
    #         "pages/super-admin.py",
    #         label="Manage admin access",
    #         disabled=st.session_state.role != "super-admin",
    #     )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("main.py", label="Home")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()
    
def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
