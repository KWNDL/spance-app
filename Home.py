'''
running the app
streamlit run /Users/kevin/PycharmProjects/spance-app/Home.py
'''

# IMPORT: External Libraries
import streamlit as st
# IMPORT: Internal libraries
from app_style import *

# Page Settings
page_settings('Home - Spance')
# Sidebar Logo
sidebar_logo('images/sp_logo_header.png')
# Page Header
header('Home')

############################
# CONTENT FUNCTIONS
############################

# Welcome Message
def home_welcome():
    st.subheader('Start your Spance journey!')
    st.markdown("Welcome to the Spance web app! Spance is a tool to get never seen insights into your cost data. \
                 How it works is relatively simple: You can upload any kind of cost data in any size and \
                 specify your organisational hierarchy, a periodical indicator and your cost amount. \
                 With the power of AI, it will then magically discover hidden patterns and trends in your data.")
# Content Overview
def home_content():
    ### HEADER
    st.subheader('Web App Content')
    st.markdown('In this app you can find the following content you can easily navigate to while simply navigating \
                 to them using the sidebar on the left side.')
    ### SPACING
    st.subheader(' ')
    ### CONTENT ICONS
    st.image('images/content/app-content.png')
# FAQ
def home_faq():
    st.subheader('FAQ')
    faq_left, faq_right = st.columns(2)
    with faq_left:
        with st.expander('How to get started?'):
            st.markdown('It is super easy! Just navigate to the Data Input page, and you can start immediately!')
        with st.expander('What is included in the app?'):
            st.markdown('The Footprints WebApp consists of three major pages:')
            st.markdown(
                '* **Data Input:** Here you submit your data to the Spance AI can work with it to find trends.')
            st.markdown('* **Data Story:** The Data Story provides you with an high-level analysis of various kinds of \
                         analysis outputs like KPIs, a periodical analysis or an outlier detection using Natural Language Generation to create dynamic commentary.')
            st.markdown(
                '* **Outlier Detection:** Detection of outliers in your data with various drill-downs to find unusual data points.')
            st.markdown(
                'These features represent a preview of some of the functionalities of the real Spance app. \
                In the **Outlook** page, we will give you some more previews of the real web app currently in the making.')
    with faq_right:
        with st.expander('Do I need to pay anything?'):
            st.markdown('The use of Spance app is a demo for the potential functions and therefore \
                         not a proper final product. It is completely free!')
        with st.expander('What happens to my data?'):
            st.markdown("The Spance app will not save any data and everything is stored and processed locally. \
            We as Spance value data privacy and security.")
            st.markdown("If you don't want to use your own data, we will provide a sample dataset.")

############################
# DISPLAY CONTENT AND FOOTER
############################

# DISPLAY: Welcome Message
home_welcome()
# DISPLAY: Content Overview
home_content()
# DISPLAY: FAQ
home_faq()
# DISPLAY: Page Footer
footer()
