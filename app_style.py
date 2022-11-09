'''
Code for HTML styling of the app for number formats
'''

# External libraries
import streamlit as st
import datetime
import base64

# App Settings and Favicon, remove menu and hide footer
def page_settings(title):
    ### PAGE TITLE AND ICON
    st.set_page_config(page_title=title,
                       page_icon='images/sp_favicon.png',
                       initial_sidebar_state='expanded')

    ### HIDE MENU
    hide_streamlit_style = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Change Font globally
    streamlit_style = """
    			<style>
    			@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400&display=swap');

    			html, body, [class*="css"]  {
    			font-family: 'Figtree', sans-serif;
    			}
    			</style>
    			"""
    st.markdown(streamlit_style, unsafe_allow_html=True)

    # Color Session States
    st.session_state['sp_color_base'] = '#FF4F00'  # orange
    st.session_state['sp_color_grey'] = '#DCDCDC'  # grey
    st.session_state['sp_color_white'] = '#FFFFFF'  # white

# Page footer
def header(page_header):
    # Push Page Up
    st.markdown('###')
    # Insert Logo
    a, b, c, = st.columns(3)
    with b:
        st.image('images/sp_logo_title.png')
    # Line
    st.markdown('---')
    st.title(page_header)

# Page footer
def footer():
    st.markdown('---')
    left, midleft, mid, midright, right = st.columns(5)
    with left:
        st.image('images/sp_logo_footer.png')
    st.caption(str(datetime.date.today().year) + ' | find us on spance.io')

def call_session_state():
    # Get Session States
    prediction = st.session_state['sp_input_df_prediction']
    raw_data = st.session_state['sp_input_df_rawdata']
    onetime = st.session_state['sp_input_df_onetimecost']
    outlier = st.session_state['sp_input_df_outlier']
    predcol_cost = st.session_state['sp_input_predcol_cost']
    predcol_hierarchy = st.session_state['sp_input_predcol_hierarchy']
    predcol_datetime = st.session_state['sp_input_predcol_datetime']
    predcol_datetime_dt = st.session_state['sp_input_predcol_datetime_dt']
    selection_currency = st.session_state['sp_input_selection_currency']
    color_base = st.session_state['sp_color_base']

    return prediction, raw_data, onetime, outlier, predcol_cost, predcol_hierarchy, predcol_datetime, predcol_datetime_dt, selection_currency, color_base

### FOOTPRINTS PREDICTION CHECK
def app_predcheck():
    check = st.session_state['sp_input_status_prediction']

# Sidebar Logo
def sidebar_logo(app_logo):
    @st.cache(allow_output_mutation=True)
    def get_base64_of_bin_file(png_file):
        with open(png_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Logo Markup and Location in Sidebar
    def build_markup_for_logo(
            png_file,
            background_position="50% 5%",
            margin_top="10%",
            image_width="87%",
            image_height="",
    ):
        binary_string = get_base64_of_bin_file(png_file)
        return """
                <style>
                    [data-testid="stSidebarNav"] {
                        background-image: url("data:image/png;base64,%s");
                        background-repeat: no-repeat;
                        background-position: %s;
                        margin-top: %s;
                        background-size: %s %s;
                    }
]                </style>
                """ % (binary_string, background_position, margin_top, image_width, image_height)

    # Add Logo
    def add_logo(png_file):
        logo_markup = build_markup_for_logo(png_file)
        st.markdown(
            logo_markup,
            unsafe_allow_html=True,
        )
    # Logo Output
    add_logo(app_logo)

# Human-readable Number format
def num_human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

# Commentary Text into white text
def html_text(text):
    color_style = '<style>.whiteText{color: #000000}</style>'
    text_format = '<span class="whiteText">{}</span>'.format(text)
    return color_style + text_format + ' '

# Commentary KPI Text into Coral color and bold
def html_highlight_text(text):
    color_style = '<style>.coralText{color: #FF4F00; font-weight: bold}</style>'
    text_format = '<span class="coralText">{}</span>'.format(text)
    return color_style + text_format

# Commentary KPI into Coral color and bold, formatting for decimal points
def html_highlight_kpi(kpi):
    color_style = '<style>.coralText{color: #FF4F00; font-weight: bold}</style>'
    text_format = '<span class="coralText">{}</span>'.format(f'{kpi:,}')
    return color_style + text_format