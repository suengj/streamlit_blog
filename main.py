from utils import myFunc as my
import os, json, time, requests
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def main():
        
    # yaml load
    with open('utils/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    # Create an authentication object (without pre_authorized)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    authenticator.login()
    
    login_status = st.session_state['authentication_status']
    # login_identifier = [if guest, the guest value should affect the following sub pages]
    
    if login_status: # if logged in

        # st.success("success")
        st.sidebar.title("홍승재의 Portfolio")
        my.sidebar_sublist() # sidebar sub list

        st.sidebar.markdown("---")

        # Main Page
        path_to_md = "./md" 

        col1, col2 = st.columns([3,1])  # section separated

        with col1:
            with open(f'{path_to_md}/main_intro.md','r') as f: 
                md_sample = f.read()
    
            st.markdown(md_sample, unsafe_allow_html=True)

        with col2:
            with open(f'{path_to_md}/main_history.md', 'r') as f:
                main_history = f.read()
    
            st.markdown(main_history, unsafe_allow_html=True)

        
    elif login_status is False:
        st.error('Username/password is incorrect')
        st.stop()
    
    elif login_status is None:
        st.warning('Please enter your username and password')
        st.stop()

if __name__ == "__main__" :
    main()

# end of code
