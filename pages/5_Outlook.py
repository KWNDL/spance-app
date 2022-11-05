# External Libraries
import streamlit as st
# Internal libraries
from app_style import *

# Page config
page_settings('Outlook - Spance')

# Sidebar Logo
sidebar_logo('images/sp_logo.png')

### FOOTPRINTS PREVIEW TEXT
def fp_preview_welcome():
    st.subheader('Just the Beginning!')
    st.markdown("This WebApp was just the beginning of the Footprints journey and gave you just a slight idea of the functionalities of the future WebApp. \
                On this page, we would like to give you some insights into the development process and the real WebApp which is currently under construction. \
                Stay tuned for future updates!")

### FOOTPRINTS PREVIEW SCREENSHOT 1
def fp_preview_scrnshot1():
    st.subheader('WebApp Home Menu')

    ### FUNCTIONALITIES
    def functionalities():
        ### FUNCTIONALITIES
        text1a = 'The Footprints interface is designed to empower you to utilise '
        text1b = 'AI capabilities '
        text1c = 'without a complex layout. We want to help you, also as a non-technical user in your organisation, \
                  to have confidence and enjoyment when using the WebApp functions. \
                  Therefore, we included '
        text1d = 'easy accessible buttons'
        text1e = 'previews '
        text1f = 'and'
        text1g = 'workflows'
        text1h = 'Our aim is to give you the feeling that everything is responsive, clear and user-friendly, \
                  so that you don’t need to seek advice from a technical person.'

        ### FINAL TEXT
        text_final = html_text(text1a) + html_highlight_text(text1b) + html_text(text1c) + \
                     html_highlight_text(text1d) + ', '+ html_highlight_text(text1e) + html_text(text1f) + \
                     html_highlight_text(text1g) + '. ' + html_text(text1h)
        return st.markdown(text_final, unsafe_allow_html=True)

    ### FUNCTION
    functionalities()
    ### SPACING
    st.subheader(' ')
    ### SCREENSHOT
    st.image('images/figma/page1.png') # FROM GITHUB
    ### CAPTION
    st.markdown("<p style='text-align: center; font-size: 14px;'>{}</p>"
                .format('Footprints WebApp starting page with functions such as New Footprints and Job Status Overview.'),
                unsafe_allow_html=True)

### FOOTPRINTS PREVIEW SCREENSHOT 2
def fp_preview_scrnshot2():
    st.subheader('Flexible Data Selection')
    ### FUNCTIONALITIES
    def functionalities():

        ### FUNCTIONALITIES
        text1a = 'To guide you seamlessly through the various functions of the Footprints WebApp, \
                  we created an easy structure to see at which step of the workflow you are at. \
                  To ensure that also your organisation can leverage the analytics capabilities,'
        text1b = 'multiple data sources '
        text1c = 'are available to be selected user-friendly and fast. We want to take you '
        text1d = 'step-by-step '
        text1e = 'through the process to view the hidden trends and patterns. \
                  Having no or less advanced data knowledge in your organisation \
                  won’t be challenging anymore as we want to '
        text1f = 'guide you through this process '
        text1g = 'with Footprints.'

        ### FINAL TEXT
        text_final = html_text(text1a) + html_highlight_text(text1b) + html_text(text1c) + \
                     html_highlight_text(text1d) + html_text(text1e) + html_highlight_text(text1f) + \
                     html_text(text1g)
        return st.markdown(text_final, unsafe_allow_html=True)

    ### FUNCTION
    functionalities()
    ### SPACING
    st.subheader(' ')
    ### SCREENSHOT
    st.image('images/figma/page2.png') # FROM GITHUB
    ### CAPTION
    st.markdown("<p style='text-align: center; font-size: 14px;'>{}</p>"
                .format('Footprints generation page with Data Source selection from various sources.'), unsafe_allow_html=True)

### FOOTPRINTS PREVIEW SCREENSHOT 3
def fp_preview_scrnshot3():
    st.subheader('Deep Cost Insights')

    ### FUNCTIONALITIES
    def functionalities():
        ### SINGLE TEXT
        text1a = 'While you will be able to generate unique insights yourself with ease - \
                  we support you in understanding these insights through'
        text1b = 'automated reporting'
        text1c = 'To showcase, present and collect relevant information, Footprints allows you to '
        text1d = 'export automated reports'
        text1e = 'presentations '
        text1f = 'and'
        text1g = 'more'
        text1h = 'Meaning that you don’t have to spend hours on getting things done on time. \
                  If you wonder which information is behind graphs, \
                  indicators and points, you can simply'
        text1i = 'see it with a click'

        ### FINAL TEXT
        text_final = html_text(text1a) + html_highlight_text(text1b) + '. '+ html_text(text1c) + \
                     html_highlight_text(text1d) + ', ' + html_highlight_text(text1e) + html_text(text1f) + \
                     html_highlight_text(text1g) + '. ' + html_text(text1h) + html_highlight_text(text1i) + '.'
        return st.markdown(text_final, unsafe_allow_html=True)

    ### FUNCTION
    functionalities()
    ### SPACING
    st.subheader(' ')
    ### SCREENSHOT
    st.image('images/figma/page3.png') # FROM GITHUB
    ### CAPTION
    st.markdown("<p style='text-align: center; font-size: 14px;'>{}</p>"
                .format('Single Footprint Analysis with various insights and dynamic commentary.'), unsafe_allow_html=True)

### FOOTPRINTS PREVIEW CLOSING
def fp_preview_outlook():
    st.subheader('And much more!')
    ### FEATURE LIST
    st.markdown('Besides this, we plan many more features such as:')
    st.markdown("""
                - Full Data Checks where every data point will be explained
                - Automated Report Generation via Drag and Drop
                - Footprints API for Developers
                """)

# Displaying the page
### PREVIEW HEADER
header('Outlook')
### PREVIEW WELCOME
fp_preview_welcome()
### SPACING
st.markdown('---')
### PREVIEW SCREENSHOT 1
fp_preview_scrnshot1()
### SPACING
st.markdown('---')
### PREVIEW SCREENSHOT 2
fp_preview_scrnshot2()
### SPACING
st.markdown('---')
### PREVIEW SCREENSHOT 3
fp_preview_scrnshot3()
### SPACING
st.markdown('---')
### PREVIEW FINAL OUTLOOK
fp_preview_outlook()
# DISPLAY: FOOTER
footer()