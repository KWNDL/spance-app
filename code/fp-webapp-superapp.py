import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import time
import altair as alt
from sklearn.ensemble import GradientBoostingRegressor
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
import os
import platform

# streamlit run /Users/kevin/PycharmProjects/spance-webapp/fp-webapp-superapp.py

############################################# HTML STYLING ################################################
###########################################################################################################

# Human readable Number format
def num_human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

# Commentary Text into white text
def html_fp_white(text):
    color_style = '<style>.whiteText{color: #FFFFFF}</style>'
    text_format = '<span class="whiteText">{}</span>'.format(text)
    return color_style + text_format + ' '

# Commentary KPI into Coral color and bold, formatting for decimal points
def html_fp_coral_kpi(kpi):
    color_style = '<style>.coralText{color: #FC776A; font-weight: bold}</style>'
    text_format = '<span class="coralText">{}</span>'.format(f'{kpi:,}')
    return color_style + text_format

# Commentary KPI Text into Coral color and bold
def html_fp_coral_text(text):
    color_style = '<style>.coralText{color: #FC776A; font-weight: bold}</style>'
    text_format = '<span class="coralText">{}</span>'.format(text)
    return color_style + text_format

# Commentary KPI into Coral color and bold, formatting for decimal points
def html_fp_blue_kpi(kpi):
    color_style = '<style>.blueText{color: #5CC8D7; font-weight: bold}</style>'
    text_format = '<span class="blueText">{}</span>'.format(f'{kpi:,}')
    return color_style + text_format

# Commentary KPI Text into Blue color and bold
def html_fp_blue_text(text):
    color_style = '<style>.blueText{color: #5CC8D7; font-weight: bold}</style>'
    text_format = '<span class="blueText">{}</span>'.format(text)
    return color_style + text_format


############################################## APP ELEMENTS #############################################
#########################################################################################################

################################## GENERAL APP FUNCTIONS ##########
###################################################################

### APP SETTINGS
def fp_app_settings():
    ### PAGE TITLE AND ICON
    st.set_page_config(page_title='Footprints WebApp', page_icon='images/fp-favicon.png')

    ### HIDE MENU
    hide_streamlit_style = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    ### PRODUCTION OR DEV CHECK
    file = '/images/fp-logo.png'
    if os.path.exists(file) == True:
        st.session_state['MODE'] = 'DEV'
    else:
        st.session_state['MODE'] = 'PROD'

### SIDEBAR SETTINGS
def fp_app_sidebar():
    ### SIDEBAR HEADER
    st.sidebar.title('WebApp Navigation')
    ### SIDEBAR PAGE SELECTION RADIO BUTTON
    page_select = st.sidebar.radio(' ',
                                   ['Home', 'Get Started', 'Data Input', 'Data Story',
                                    'Outlier Detection', 'Feedback', 'Outlook'])
    ### SIGN OUT BUTTON
    if st.sidebar.button('Start Again'):
        st.session_state['LOGIN'] = False
        st.session_state['RESTART'] = True
        caching.clear_cache()
    ### LOGIN STATUS
    return page_select

### FOOTPRINTS PAGE FOOTER
def fp_app_footer():
    st.markdown('---')
    left, midleft, mid, midright, right = st.columns(5)
    with left:
        st.image('images/fp-logo.png')
    st.caption('Visit us on [www.footprints.digital](http://www.footprints.digital) or contact us via [hello@footprints.digital](mailto:hello@footprints.digital).')

### FOOTPRINTS PREDICTION CHECK
def fp_app_predcheck():
    check = st.session_state['prediction']

### FOOTPRINTS MAIL NOTIF
def fp_app_notification(type,df):
    ### CREDENTIALS
    sender = 'reports@footprints.digital'
    sender_pass = 'Hz5_!2sDcL'
    receiver = 'reports@footprints.digital'

    ### EMAIL MESSAGE TEXT
    message = """
    There was a new {} by a user!

    First Name: {}
    Last Name: {}
    Email: {}
    Time: {}
    Session ID: {}

    Attached the file with the information.
    """.format(type,
               st.session_state['FIRST_NAME'],
               st.session_state['LAST_NAME'],
               st.session_state['EMAIL'],
               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               st.session_state['SESSION_ID'])

    ### ADD FROM / TO / DATE
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = sender
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Footprints WebApp - New {} - Session ID: '.format(type) + st.session_state['SESSION_ID']

    ### ATTACH TO MESSAGE
    msg.attach(MIMEText(message))

    ### ATTACH FILE TO MESSAGE
    df_csv = df.to_csv()
    part = MIMEBase('application', "octet-stream")
    part.set_payload(df_csv)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{}_{}.csv"'.format(type,st.session_state['SESSION_ID']))
    msg.attach(part)

    ### SEND EMAIL
    server = smtplib.SMTP_SSL('smtp.hostinger.com', 465)  # use gmail with port
    server.login(sender, sender_pass)
    server.sendmail(sender, receiver, msg.as_string())
    server.close()


################################# WELCOME PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_home_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Footprints WebApp')
    with titleright:
        st.image('images/fp-logo.png')

### FOOTPRINTS WELCOMING TEXT
def fp_home_welcome():
    st.subheader('Start your Footprints journey!')
    st.markdown("Welcome to the Footprints WebApp! Footprints is a revolutionary tool to get never seen insights into your cost data. \
                 How it works is relatively simple. You can upload any kind of cost data, doesn't matter how big it is, \
                 specify your organisational hierarchy, a periodical indicator and your cost data. \
                 From there, the power of the Footprints AI will magicly discover hidden patterns and trends in your data to give you unique insights into your data to unveil the unseen.")

### FOOTPRINTS CONTENT
def fp_home_content():
    ### HEADER
    st.subheader('WebApp Content')
    st.markdown('In the WebApp you can find the following content you can easily navigate to while simply navigating \
                 to them using the sidebar on the left side.')
    ### SPACING
    st.subheader(' ')
    ### CONTENT ICONS
    st.image('images/content/app-content.png')

### FOOTPRINTS FAQ SECTION
def fp_home_faq():
    st.subheader('FAQ')

    faq_left, faq_right = st.columns(2)
    with faq_left:
        with st.expander('How to get started?'):
            st.markdown('It is super easy! Just navigate to the Get Started page, leave your mail address there and \
                        you can start using the first preview of the Footprints WebApp!')
        with st.expander('What is included in the Footprints WebApp?'):
            st.markdown('The Footprints WebApp consists of three major pages:')
            st.markdown(
                '* **Data Input:** Here you submit your data that the Footprint AI can work with it to find trends.')
            st.markdown('* **Data Story:** The Data Story provides you with an high-level analysis of varous kinds of \
                         analysis outputs like overall KPIs, a periodical analysis or an outlier detection using Natural Language Generation (NLG) to create dynamic commentary.')
            st.markdown(
                '* **Outlier Detection:** Detection of outliers in your data with various drill-downs to find unusual data points.')
            st.markdown(
                'These features all represent a preview of some functionalities of the real Footprints app coming soon. \
                Additionally, there is the **Feedback** page to share your experiences with us as well as the **Outlook** page to give a preview of the real WebApp currently under construction.')
    with faq_right:
        with st.expander('Do I need to pay anything?'):
            st.markdown('The use of the Footprints WebApp is a demo for the potential functions and therefore \
                         not a proper final product. It is completely free!')
        with st.expander('What happens to my data?'):
            st.markdown("The Footprints WebApp is build in a way that there won't be any data saved somewhere and everything is stored locally in your cache. \
            We as Footprints value data privacy and promise that no data, except the optional usage metrics, will be saved.")
            st.markdown("If you don't want to use your own data, we will provide a dataset once you're in.")


################################### LOGIN PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_login_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Footprints Get Started')
    with titleright:
        st.image('images/fp-logo.png')

### FOOTPRINTS WELCOMING TEXT
def fp_login_welcome():
    st.subheader('Start your Footprints journey!')
    st.markdown("Before you get a first taste of Footprints functions, please tell us more about you. \
                 For that, simply use your email address you used to get started. \
                 Keep in mind that this app is still a preview and not a final product. \
                 Therefore, you have five tries to run predictions and get insights.")

### FOOTPRINTS LOGIN FORM
def fp_login_submit():
    ### TITLE
    st.subheader('Tell us more about you to get started')
    with st.form("my_form"):

        form_left, form_mid, form_right = st.columns(3)
        with form_left:
            first_name = st.text_input('First Name')
        with form_mid:
            last_name = st.text_input('Last Name')
        with form_right:
            occupation = st.selectbox('Occupation',['Business Owner','Employee','Student','Others'])

        email = st.text_input('Your Email address')
        tracing = st.checkbox('I agree to share my usage behaviour in the Footprints WebApp to support any future improvements. (Not working yet!) *',
                               help='Footprints will collect anonymously usage behaviour from using the app. \
                               This includes for example the app perfomance, data size or the number of footprints generated.\
                               Footprints will not trace any personal data or save any confidential information.',
                               value=True)
        st.caption('*Selection is optional.')

        ### Submit Button, then switch status to True
        submitted = st.form_submit_button("Get Started")
        fp_login_submit.submit_status = True

        ### No hierarchy = Error
        if submitted:
            if (not first_name) | (not last_name):
                st.error('Please tell us your name!')
            elif not email:
                st.error('Please enter an email address!')
            elif '@' not in email:
                st.error('Please enter a valid email address.')
            elif '.' not in email:
                st.error('Please enter a valid email address.')
            else:
                ### SUCCESS NOTIFICATION
                st.success('Hi {} {}, welcome to Footprints! We are happy to have you! \
                            You can now start under the Data Input page'.format(first_name,last_name))
                st.session_state['FIRST_NAME'] = first_name
                st.session_state['LAST_NAME'] = last_name
                st.session_state['EMAIL'] = email
                st.session_state['LOGIN'] = True
                st.session_state['SESSION_ID'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))

                ### CREATE FINAL TABLE FOR LOGIN
                user_login = [[first_name,last_name,occupation,email,tracing]]
                user_df = pd.DataFrame(user_login)
                user_df.columns = ['FIRST_NAME','LAST_NAME','OCCUPATION','EMAIL','TRACING']
                user_df['START_TIME'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    user_df['OPERATING_SYSTEM'] = str(platform.system())
                    user_df['OPERATING_SYSTEM_RELEASE'] = str(platform.release())
                except:
                    user_df['OPERATING_SYSTEM'] = 'N/A'
                    user_df['OPERATING_SYSTEM_RELEASE'] = 'N/A'
                user_df['SESSION_ID'] = st.session_state['SESSION_ID']

                ### WRITE DATA TO CSV
                try:
                    ### OFFLINE
                    user_df.to_csv('/Users/kevin/Google Drive/.shortcut-targets-by-id/1pkEbWCt9mdIhGXKn6vnn6IIbA3LUbWuI/Footprints Start-Up /Data Repository/fp-user-login.csv', mode='a', index=False, header=False)
                except:
                    ### DEPLOYMENT
                    type = 'Login'
                    fp_app_notification(type,user_df)


############################## DATA INPUT PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_input_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Footprints Data Input')
    with titleright:
        st.image('images/fp-logo.png')

### FOOTPRINTS WELCOMING TEXT
def fp_input_welcome():
    st.subheader('With the Power of the Footprints AI!')
    st.markdown("Now we're ready to experience a whole new experience of AI and Machine Learning to get never seen insights \
                 from your data. On this page, simply upload your cost data files in CSV or Excel format or pick the \
                 sample data provided by Footprints. Then, you simply select the cost column, a data column and any \
                 kind of hierarchy within your data. Then it's ready for the Footprints AI to be analyzed!")

### FOOTPRINTS DATA UPLOAD
def fp_input_upload():
    ### FILE UPLOAD
    st.subheader('Uploading Data')
    st.markdown('In the beginning, there was data. Therefore, we need to upload some data. But you have the choice \
                 upload your own data or pick the Footprints sample. In case you chose your own example, the maximum \
                 size is 200MB.')
    # SELECTBOX EITHER SAMPLE DATA OR UPLOAD OWN DATA
    upload_select = st.selectbox('Pick the data source',['Upload own Data','Footprints Sample Data'])

    ### FUNCTION FOR FILE SELECTION: EITHER FP SAMPLE OR OWN DATA
    def file_selection(upload_select):
        if upload_select == 'Footprints Sample Data':
            try:
                cost_data = pd.read_csv('/Users/kevin/Google Drive/.shortcut-targets-by-id/1pkEbWCt9mdIhGXKn6vnn6IIbA3LUbWuI/Footprints Start-Up /Data Repository/fp-data.csv')
            except:
                cost_data = pd.read_csv('../data/fp-data.csv')
            cost_data = pd.DataFrame(cost_data)
            st.session_state['raw-data'] = cost_data
            st.success('Footprints Sample Data loaded successfully!')
            return cost_data
        elif upload_select == 'Upload own Data':
            file_upload = st.file_uploader("Upload", type=['csv'])
            if file_upload != None:
                cost_data = pd.read_csv(file_upload)
                cost_data = pd.DataFrame(cost_data)
                st.session_state['raw-data'] = cost_data
                st.success('You uploaded your own data successfully!')
                return cost_data
            else:
                fp_app_footer()
                st.stop()

    ### DISPLAY COST DATA
    cost_data = file_selection(upload_select)
    st.subheader('Data Preview')
    if upload_select == 'Footprints Sample Data':
        st.markdown(
            'The Footprints Sample Data has been successfully loaded and it can be used now. \
             To have a first data preview, here are 1000 randomly selected rows.')
    elif upload_select == 'Upload own Data':
        st.markdown(
            'You successfully uploaded a file and it can be used now. \
             To have a first data preview, here are 1000 randomly selected rows.')

    cost_data_display = cost_data.head(1000).sample(frac=1).reset_index(drop=True)
    cost_data_display.index += 1
    st.write(cost_data_display)

    ### DATA ROW AND COLUMN COUNT COMMENTARY
    def input_commentary():
        # ROW AND COLUMN COUNT KPIs
        cost_data_rows = len(cost_data)
        cost_data_cols = len(cost_data.columns)

        # TEXT FOR COMMENTARY
        if upload_select == 'Footprints Sample Data':
            text1a = 'The sample data has'
        else:
            text1a = 'The uploaded data has'
        text1b = ' rows and'
        text1c = ' columns in total.'

        # FINAL TEXT
        text_final = html_fp_white(text1a) + html_fp_coral_kpi(cost_data_rows) + html_fp_white(text1b) + \
                     html_fp_coral_kpi(cost_data_cols) + html_fp_white(text1c)
        return text_final
    st.markdown(input_commentary(),unsafe_allow_html=True)

    ### EXPANDER BOX SAMPLE DATA
    st.subheader('  ')
    if upload_select == 'Footprints Sample Data':
        with st.expander('What do the Sample Data columns stand for?'):
            st.markdown("""
                        The Footprints Sample Data is based on the **fictional Footprints Group** with multiple companies 
                        across different countries and sites. The dataset contains data on a **transactional level** \
                        which means that every single row shows one single spending.
                        
                        Since the data is slightly complex and relatively big, here is an explanation of what the columns mean:
                        - **Amount Euro:** Actual Spending in Euro
                        - **Date Calendar Month:** Month of the Transaction
                        - **Cost Type:** Single Type and most detailed kind of costs
                        - **Cost Type Level:** Cost structure Hierarchy in three levels with level 1 highest
                        - **Cost Center:** Cost Center number where the spending belongs to
                        - **Person Responsible:** Responsible person of the cost center
                        - **Date Document:** Date of the Transaction
                        - **Document Number:** Unique Transactional Document Number
                        - **Fix Var:** Indicator Fix or Variable Costs
                        - **Prim Sec:** Indicator Primary or Secondary Costs
                        - **Country:** Country of Cost Origin
                        - **Company:** Footprints Company Name
                        - **Company Site:** Location of Company
                        - **Unit and Sub Unit:** Business Organizational Structure
                        """)

    ### FINAL CHECK THAT FILE UPLOADED, THEN RETURN TABLE
    file_uploaded = True
    return cost_data, file_uploaded

### FOOTPRINTS HIERARCHY SELECTION
def fp_input_hierarchy():
    ### OPENING TEXT
    st.subheader('Hierarchy Selection')
    st.markdown("""
                Footprints is based on three types of columns in order to run:
                - **Cost Column:** Numerical that contains cost amount 
                - **Datetime Column:** Column that indicates the time when the spending has been made
                - **Multiple Hierarchy Columns:** Combination of column for cost insights
                
                All together will define the dimension of your cost insights.
                """)
    st.subheader('  ')

    # EXTRACT COLUMN LIST DEPENDING ON THE TYPE
    num_cols = cost_data.select_dtypes(include=np.number).columns.tolist()
    str_cols = cost_data.select_dtypes(include=np.object_).columns.tolist()

    ### FIND DATETIME COLUMNS
    def date_columns():
        cd = cost_data.copy()
        date_cols = []
        for col in str_cols:
            try:
                pd.to_datetime(cd[col])
                date_cols.append(col)
            except:
                pass
        return date_cols
    date_cols = date_columns()

    ### FORM HIERARCHY SELECTION
    with st.form('Hierarchy Selection'):
        ### SELECT COST COLUMN AND CURRENCY
        st.markdown('Select Cost Column and the respective currency.')
        left_col, right_col = st.columns(2)
        with left_col:
            sel_costcol = st.selectbox('Cost Column', options=num_cols)
            st.session_state['cost-col'] = sel_costcol
        with right_col:
            sel_currency = st.selectbox('Currency',['EUR','USD','AUD','SGD','MYR','CNY'])
            st.session_state['currency'] = sel_currency

        ### SELECT DATETIME COLUMN AND GRANULARITY
        st.markdown('Select Datetime column and the granularity of it.')

        left_col, right_col = st.columns(2)
        with left_col:
            sel_datetime = st.selectbox('Datetime Column', options=date_cols)
            st.session_state['datetime'] = sel_datetime
        with right_col:
            sel_granularity = st.selectbox('Time Granularity (available very soon!)', ['Month', 'Week', 'Day'],
                                           help='Currently inactive.')
            st.session_state['granularity'] = sel_granularity

        ### SELECT HIERARCHY COLUMNS
        st.markdown(
            'Next, select hierarchy columns in order to specify on with level \
             you want to create your footprints. A particular order is not required.')
        hier_cols = [col for col in str_cols if col not in date_cols]
        sel_hierarchy = st.multiselect('Hierarchy Columns', options=hier_cols, help='No maximum hierarchies.')
        st.session_state['hier-cols'] = sel_hierarchy

        ### SUBMIT BUTTON
        submitted = st.form_submit_button("Confirm Hierarchy")
        if submitted:
            ### HIER STATUS
            st.session_state['HIER_STATUS'] = True
            ### DISPLAY HIERARCHY OVERVIEW
            def hierarchy_overview():
                ### INTRODUCTION TEXT
                st.subheader('Hierarchy Overview')
                st.markdown('Now it is about to time to run the data transformation to bring the data in shape according to your selected values. \
                                          Down below you see an overview of your selected hierarchies.')

                ### FIND HIERARCHY COLUMN HIERARCHY
                hier_name = [];
                hier_count = []

                for col in sel_hierarchy:
                    hier_name.append(col)
                    hier_count.append(len(cost_data[col].unique()))

                    hier_level = pd.DataFrame({'HIERARCHY_NAME': hier_name, 'HIERARCHY_VALUES': hier_count}) \
                        .sort_values('HIERARCHY_VALUES', ascending=True).reset_index()
                    hier_level['index'] = hier_level.index
                    hier_level['index'] += 1
                    hier_level = hier_level.rename(columns={'index': 'HIERARCHY_LEVEL'})
                    hier_level.index += 1
                    st.session_state['hier-level'] = hier_level

                ### WRITE HIERARCHY TABLE
                st.write(hier_level)

                ### CREATE HIERARCHY COMMENTARY
                def commentary():
                    ### HIERARCHY KPIs
                    loop_list = cost_data.groupby(sel_hierarchy, as_index=False).size().drop('size',
                                                                                             axis=1).reset_index()
                    footprint_count = len(loop_list)
                    footprint_hier = len(sel_hierarchy)

                    ### COMMENTARIES
                    text1a = 'With the hierarchies selected, a total of'
                    text1b = ' Footprints'
                    text1c = ' across'
                    if len(sel_hierarchy) == 1:
                        text1d = ' Hierarchy'
                    else:
                        text1d = ' Hierarchies'
                    text1e = ' will be generated.'

                    ### CREATE FINAL TEXT
                    final_text = html_fp_white(text1a) + html_fp_coral_kpi(footprint_count) + html_fp_coral_text(
                        text1b) + \
                                 html_fp_white(text1c) + html_fp_coral_kpi(footprint_hier) + html_fp_coral_text(
                        text1d) + \
                                 html_fp_white(text1e)
                    return final_text

                ### FINAL COMMENTARY
                st.markdown(commentary(), unsafe_allow_html=True)
                hier_status = True
                return hier_status
            hierarchy_overview()
            ### SPACING
            st.subheader('  ')

    ### PROCEED WHEN HIERARCHY IS SELECTED
    if len(sel_hierarchy) != 0:
        submit_status = True
        hier_status = st.session_state['HIER_STATUS']
        return submit_status, sel_costcol, sel_datetime, sel_hierarchy, sel_currency, hier_status
    else:
        fp_app_footer()
        st.stop()

### FOOTPRINTS DATA TRANSFORMATION
def fp_input_ml_transformation():

        ### INTRODUCTION TEXT
        st.subheader('Generate Footprints')
        st.markdown('As the final step, we are now ready to generate Footprints based your given data and the hierarchy.')

        ### DATA PREPARATION
        cost_data['VAL_BOOKING_COUNT'] = 1
        data_gb = cost_data.groupby(by=sel_hierarchy, as_index=False).size()

        # Filter Data for One Time Costs (=1) and Multiple Time Costs (>1), Multi used for Prediction
        cost_pred = data_gb[data_gb['size'] > 1]
        cost_onetime = data_gb[data_gb['size'] == 1]

        # Create Unique GroupBy Lists
        cost_pred = cost_pred.drop('size', axis=1)
        cost_onetime = cost_onetime.drop('size', axis=1)

        # Join and Filter Datasets
        cost_pred = pd.merge(cost_data, cost_pred, on=sel_hierarchy, how='inner')
        cost_onetime = pd.merge(cost_data, cost_onetime, on=sel_hierarchy, how='inner')

        # Create Loop List, GroupBy Multi Entries by Hierarchy + Month, Calculate KPIs
        loop_list = cost_pred.groupby(sel_hierarchy, as_index=False).size().drop('size', axis=1).reset_index()
        loop_list = loop_list.rename(columns={'index': 'LOOP_ID'})
        loop_list['LOOP_ID'] += 1

        # GroupBy Multi Entries by Hierarchy + Month, Calculate Total Costs and Bookings, then add Loop ID
        cost_pred = cost_pred.groupby(pred_col, as_index=False).sum()
        cost_pred = pd.merge(cost_pred, loop_list, on=sel_hierarchy, how='left')

        ### CREATE MONTH COLUMN
        cost_pred['CAL_CALENDAR_MONTH'] = pd.DatetimeIndex(cost_pred[sel_datetime]).month
        cost_pred['CAL_CALENDAR_YEAR'] = pd.DatetimeIndex(cost_pred[sel_datetime]).year

        ### TRANSFORM STATUS TRUE
        transform_status = True
        st.session_state['one-time-costs'] = cost_onetime
        return transform_status, cost_pred, cost_onetime, loop_list

### FOOTPRINTS COST BAND PREDICTION
def fp_input_ml_prediction():

    ### MESSAGE DATA TRANSFORMATION DONE
    time.sleep(0.5)
    fp_count = len(loop_list) + len(cost_onetime)
    st.success('Automated Data Transformation completed.')
    st.success('Out of {} Footprints, {} One-Time costs were detected. \
                The {} remaining Footprints will be generated.'.format(fp_count, len(cost_onetime), len(loop_list)))
    time.sleep(0.5)

    ### PROGRESS BAR + COLORING
    st.markdown('<style>.stProgress.st-bo{background-color: #FC776A}</style>', unsafe_allow_html=True)
    latest_iteration = st.empty()
    bar = st.progress(0)
    start_time = datetime.now()

    ### DATAFRAMES FOR PREDICTIONS
    final_pred = pd.DataFrame([])
    norm_set = pd.DataFrame([])

    ### PREDICTIONS
    for loop_id in range(1, len(loop_list) + 1):

        ### SELECT THE RESPECTIVE LOOP ROUND
        pred_set = cost_pred[cost_pred['LOOP_ID'] == loop_id]

        ### ITERATION HIERARCHY VALUES
        col_value = ''
        for col in sel_hierarchy:
            col_names = pred_set[col].iloc[0]
            if col_value == '':
                col_value += col_names
            else:
                col_value += ' + ' + col_names

        ### CREATE STD DATASET
        pred_std = pred_set[sel_costcol]
        cost_col_norm = str(sel_costcol) + '_NORM'
        pred_std = pd.DataFrame(pred_std).rename(columns={sel_costcol:cost_col_norm})


        ### Z-SCORE FUNCTION, THEN APPLY ON STD DATASET
        def z_score(df):
            # COPY DATAFRAME
            df_std = df.copy()
            ### APPLY Z-SCORE METHOD
            for column in df_std.columns:
                df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
            return df_std

        ### APPLY Z-NORMALIZATION FUNCTION TO DATASET
        pred_std = z_score(pred_std)
        pred_set = pd.concat([pred_set, pred_std], axis=1, sort=False).reset_index()

        ### FINAL TABLES FOR ML WITH THRESHOLD FOR TRAINING DATASET
        threshold = 1.5
        cost_final = pred_set.drop([cost_col_norm], axis=1)
        pred_set = pred_set[
            (pred_set[cost_col_norm] < threshold) & (pred_set[cost_col_norm] > -threshold)].drop(
            [cost_col_norm], axis=1)

        ### TRAINING SET
        X = pred_set[['CAL_CALENDAR_MONTH', 'CAL_CALENDAR_YEAR', 'VAL_BOOKING_COUNT']]
        y = pred_set[sel_costcol]

        ### DEAL WITH SMALL TABLES: IF TOO SMALL THEN PRED = ACT /// ELSE: PREDICTION
        if len(X) == 0:
            cost_final['VALUE_PREDICTION'] = 0.0
        else:
            ### APPLY GBT AND PREDICT COSTS
            gbt = GradientBoostingRegressor(max_depth=4, alpha=0.95, max_leaf_nodes=4, n_estimators=25)
            gbt.fit(X, np.ravel(y))

        ### PREDICTION ON ACTUAL DATA
        prediction = cost_final[['CAL_CALENDAR_MONTH', 'CAL_CALENDAR_YEAR', 'VAL_BOOKING_COUNT']]
        prediction = gbt.predict(prediction)
        cost_final['VALUE_PREDICTION'] = prediction

        ### APPEND EVERYTHING TO FINAL DATASET
        final_pred = final_pred.append(cost_final)
        norm_set = norm_set.append(pred_set)

        ### DISPLAY PROGRESS BAR
        progress_time = datetime.now() - start_time
        iteration_text = 'Progress: ' + str(str(loop_id / len(loop_list) * 100)[:6]) + '% // Footprint ' + str(loop_id) + ' out of ' + str(len(loop_list)) + ' // Runtime: ' + str(progress_time)
        latest_iteration.text(iteration_text)
        bar.progress(loop_id / len(loop_list))

    ### RUNTIME CALCULATION
    runtime = datetime.now() - start_time
    runtime_min = runtime.seconds / 60
    runtime_sec = runtime.seconds

    if runtime_min > 1:
        runtime_min_s = round(runtime_sec - (int(runtime_min) * 60),0)
        if runtime_min_s != 0:
            runtime_clean = str(int(round(runtime_min,0))) + 'm ' + str(round(runtime_min_s,0)) + 's'
        else: runtime_clean = str(round(runtime_min,0)) + 'm'
    else:
        runtime_clean = str(runtime_sec) + 's'
    st.success('Footprint Generation completed!')

    ### FINAL OUTPUT
    pred_status = True
    st.session_state['PREDICTION_COMPLETE'] = True
    return pred_status, runtime_clean, final_pred, norm_set

### FOOTPRINTS CONSTRUCT FINAL DATASET
def fp_input_ml_construct(norm_set):

    ### INTRODUCTION TEXT
    st.subheader('Predicted Footprints')
    st.markdown('All cost footprints have been fully generated. To start off, here are some KPIs.')

    ### GENERATE STD FOR EACH LOOP + YEAR
    cost_col_std = str(sel_costcol) + '_STD'
    norm_set = norm_set.groupby(by=['LOOP_ID', 'CAL_CALENDAR_YEAR'], as_index=False).agg(np.std).rename(
        columns={sel_costcol: cost_col_std})
    norm_set = norm_set[['LOOP_ID', 'CAL_CALENDAR_YEAR', cost_col_std]]

    ### JOIN STD WITH MAIN DATASET
    fp = pd.merge(final_pred, norm_set, on=['LOOP_ID', 'CAL_CALENDAR_YEAR'], how='left').fillna(0.0)

    ### UPPER AND LOWER BOUND
    fp['FP_UPPER_BOUND'] = fp['VALUE_PREDICTION'] + fp[cost_col_std]
    fp['FP_LOWER_BOUND'] = fp['VALUE_PREDICTION'] - fp[cost_col_std]

    ### RATING TOO LOW / TOO HIGH
    fp['FP_RATING'] = np.where(fp[sel_costcol] > fp['FP_UPPER_BOUND'], 'Too High',
                               np.where(fp[sel_costcol] < fp['FP_LOWER_BOUND'], 'Too Low',
                                        'Okay'))

    ### CALCULATE ABSOLUTE DEVIATION
    fp['FP_DEV_ABS'] = np.where(fp['FP_RATING'] == 'Too High', fp[sel_costcol] - fp['FP_UPPER_BOUND'],
                                np.where(fp['FP_RATING'] == 'Too Low', fp['FP_LOWER_BOUND'] - fp[sel_costcol],
                                         0.0))

    ### CALCULATE ABSOLUTE DEVIATION
    fp['FP_DEV_REL'] = np.where(fp['FP_RATING'] == 'Too High', (fp[sel_costcol] / fp['FP_UPPER_BOUND'] - 1),
                                np.where(fp['FP_RATING'] == 'Too Low', (1 - (fp[sel_costcol] / fp['FP_LOWER_BOUND'])),
                                         0.0))

    ### ADD LOAD DATE CLEANUP
    fp = fp.round(2)
    fp = fp.drop('index',axis=1)

    ### CALCULATE KPIs
    prediction_amount = fp.sum()[sel_costcol]
    prediction_count = len(fp)
    footprints_gen = len(loop_list) + len(cost_onetime)

    ### KPI BOXES
    kpileft, kpimidleft, kpimidright, kpiright = st.columns(4)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                runtime), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Prediction Runtime</h3>",
                    unsafe_allow_html=True)
    with kpimidleft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                num_human_format(prediction_amount)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Analyzed Costs in {}</h3>".format(st.session_state['currency']), unsafe_allow_html=True)
    with kpimidright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{prediction_count:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Total Predictions Made</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{footprints_gen:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Footprints Generated</h3>", unsafe_allow_html=True)

    ### PRINT PREDICTION TABLE AND WRAP UP
    st.title(' ')
    st.markdown('This is a preview of the first 1000 columns of the final prediction.')

    fp_final = fp.drop(['LOOP_ID','VALUE_PREDICTION',cost_col_std],axis=1)
    fp_final.index += 1
    st.write(fp_final.head(1000))

    st.markdown('Now, the **Data Story** and the **Outlier Detection** are available \
                 to be explored to gain more insights from the cost data.')
    return fp


############################## DATA STORY PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_datastory_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Footprints Data Story')
    with titleright:
        st.image('images/fp-logo.png')

### FOOTPRINTS WELCOMING TEXT
def fp_datastory_welcome():
    st.subheader('Telling your Data Story!')
    st.markdown("After successfully generating your unique cost footprints, it is about time to dive deeper into \
                deeper into your data. You can find 5 different sections explaining various kinds of areas of your \
                data as a starting point for a deeper analysis.")

### FOOTPRINTS DATA STORY OVERALL KPIs
def fp_datastory_kpis():
    st.header('Overall KPIs')
    st.write('Before we start diving deeper into the data, lets get an overall look at the most important KPIs based on the predictions.')

    prediction = st.session_state['prediction']
    sel_hierarchy = st.session_state['hier-cols']

    ### CALCULATE KPIs
    prediction_amount = prediction.sum()[st.session_state['cost-col']]
    prediction_count = len(prediction)
    footprints_gen = len(prediction.groupby(by=sel_hierarchy, axis=0, as_index=False).size())

    ### KPI BOXES
    kpileft, kpimid, kpiright = st.columns(3)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                num_human_format(prediction_amount)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Analyzed Costs in {}</h3>".format(st.session_state['currency']), unsafe_allow_html=True)
    with kpimid:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{prediction_count:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Predictions Made</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{footprints_gen:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Footprints Generated</h3>", unsafe_allow_html=True)

### FOOTPRINTS DATA STORY COST DRIVERS
def fp_datastory_costdriver():
    # Section Header
    st.header('Main Cost Drivers')
    st.write(
        'First, we will have a look into the top cost drivers by hierarchy level. For that, please select one of your hierarchy columns to start investigate your data to find the biggest cost drivers.')

    prediction = st.session_state['prediction']
    sel_costcol = st.session_state['cost-col']
    sel_hier = st.session_state['hier-cols']
    sel_currency = st.session_state['currency']

    # Hierarchy Column Selection, Top N Selection
    headleft, headright = st.columns(2)
    with headleft:
        sel_col = st.selectbox('Select a Hierarchy Column', sel_hier)
    with headright:
        topN = st.number_input('Select Top N', 2, 20, 10)

    ### TOP N TABLE
    fp_costdriver = prediction.groupby(by=sel_col, axis=0, as_index=False).sum(sel_costcol)
    fp_topn_costdriver = fp_costdriver.sort_values(by=sel_costcol, axis=0, ascending=False).head(int(topN))
    fp_topn_costdriver = fp_topn_costdriver.sort_values(by=sel_costcol, axis=0, ascending=False)

    ### HINT THAT N IS BIGGER THAN TABLE LENGTH
    if topN > len(fp_costdriver):
        st.info('The selected N is higher than the number of available values. \
                 The maximum number is {}.'.format(str(len(fp_costdriver))))

    ### COMMENTARY
    def commentary():
        ### GENERATE KPIs
        topn_amount = fp_topn_costdriver[sel_costcol].sum()
        fp_totalamt = prediction[sel_costcol].sum()

        # TEXT GENERATION 1
        text1a = 'The top '
        text1b = ' values by the overall amount in ' + sel_currency + ' for'
        text1c = ' have been selected.'

        ### TEXT1 FINAL
        text1_final = html_fp_white(text1a) + html_fp_coral_kpi(int(topN)) + \
                      html_fp_white(text1b) + html_fp_coral_text(sel_col) + html_fp_white(text1c)

        # TEXT GENERATION 2
        text2a = 'Their total amount equals '
        text2b = ' which makes up more than '
        text2c = ' of the total overall cost of '
        text2d = ' in the data.'
        total_perc = str(round((topn_amount / fp_totalamt * 100), 2)) + '%'

        ### TEXT2 FINAL
        text2_final = html_fp_white(text2a) + html_fp_coral_text(num_human_format(topn_amount)) + ' ' + \
                      html_fp_coral_text(sel_currency) + html_fp_white(text2b) + \
                      html_fp_coral_text(total_perc) + html_fp_white(text2c) + \
                      html_fp_coral_text(num_human_format(fp_totalamt)) + html_fp_white(text2d)

        ### TEXT GENERATION 3
        text3a = 'The single highest cost driver is '  ### top 1 element
        text3b = ' with '  # Cost amount
        text3c = ' in total.'  ### difference to 2nd
        top1 = fp_topn_costdriver[sel_col].iloc[0]
        cost_col = st.session_state['cost-col']
        top1_amnt = fp_topn_costdriver[fp_topn_costdriver[sel_col] == top1][cost_col].iloc[0]

        ### TEXT4 FINAL
        text3_final = html_fp_white(text3a) + html_fp_coral_text(top1) + html_fp_white(text3b) + \
                      html_fp_coral_text(num_human_format(top1_amnt)) + html_fp_white(text3c)

        if topN >= len(fp_costdriver):
            return text1_final + text2_final + text3_final
        else:
            ### TEXT GENERATION 3
            text3a = 'The remaining '  # X Amount in Euro
            text3b = ' are shared amongst the other '  # other combinations for the selected columns
            text3c = ' available values for the selected Hierarchy Column. '
            diff_amnt = fp_totalamt - topn_amount
            unique_fp = len(fp_costdriver) - int(topN)

            ### TEXT3 FINAL
            text3_final = html_fp_white(text3a) + html_fp_coral_text(num_human_format(diff_amnt)) + \
                          html_fp_white(text3b) + html_fp_coral_kpi(unique_fp) + html_fp_white(text3c)

            ### TEXT GENERATION 4
            text4a = 'The single highest cost driver is '  ### top 1 element
            text4b = ' with '  # Cost amount
            text4c = ' in total.'  ### difference to 2nd
            top1 = fp_topn_costdriver[sel_col].iloc[0]
            cost_col = st.session_state['cost-col']
            top1_amnt = fp_topn_costdriver[fp_topn_costdriver[sel_col] == top1][cost_col].iloc[0]

            ### TEXT4 FINAL
            text4_final = html_fp_white(text4a) + html_fp_coral_text(top1) + html_fp_white(text4b) + \
                          html_fp_coral_text(num_human_format(top1_amnt)) + html_fp_white(text4c)

            return text1_final + text2_final + text3_final + text4_final

    ### CHART FOR LOWER BOUND
    chart = alt.Chart(fp_topn_costdriver).mark_bar(size=12)\
        .encode(x=alt.X(sel_costcol),
                y=alt.Y(sel_col, sort='-x'),
                color=alt.value('#5CC8D7'),
                tooltip=[sel_costcol])\
        .interactive()

    ### CHART AND COMMENTARY
    st.title(' ')
    st.altair_chart(chart,use_container_width=True)
    st.markdown(commentary(), unsafe_allow_html=True)

### FOOTPRINTS DATA STORY PERIODICAL ANALYSIS
def fp_datastory_periods():
    ### Section Header, Spacing and Column Split
    st.header('Periodical Analysis')
    st.write('Next, we look into the periodical overview of your analyzed costs.')

    ### KPIs
    date_col = st.session_state['datetime']
    cost_col = st.session_state['cost-col']
    currency = st.session_state['currency']

    ### PREDICTION DATA
    fp = st.session_state['prediction']
    fp_period = fp.groupby(by=date_col, axis=0, as_index=False).sum(cost_col)

    ### COMMENTARY
    def commentary():
        # TEXT GENERATION 1
        text1a = 'The costs have been analyzed in a period from'
        text1b = ' to '
        text1c = ' across '
        text1d = ' different periods.'
        period_first = fp_period[date_col].min()  # First Month
        period_last = fp_period[date_col].max()  # Last Month
        period_list = fp_period[date_col].unique()  # Unique List of all the years
        period_count = len(period_list)  # Number of Years

        # TEXT GENERATION 2
        text2a = ' During this time, the average spend has been '
        text2b = ' per month.'
        text2c = ' The highest spend was during '
        text2d = ' with an total amount of '
        text2e = ' while '
        text2f = ' with a total of '
        text2g = ' being the lowest.'

        ### TEXT 2 KPIs
        period_avg = fp_period[cost_col].mean()
        value_max = fp_period[cost_col].max()
        value_min = fp_period[cost_col].min()
        per_val_max = fp_period[fp_period[cost_col] == value_max][date_col].iloc[0]
        per_val_min = fp_period[fp_period[cost_col] == value_min][date_col].iloc[0]

        # FINAL COMMENTARY
        text1_final = html_fp_white(text1a) + html_fp_coral_text(period_first) + html_fp_white(text1b) + \
                      html_fp_coral_text(period_last) + html_fp_white(text1c) + html_fp_coral_kpi(period_count) + \
                      html_fp_white(text1d)

        text2_final = html_fp_white(text2a) + html_fp_coral_text(num_human_format(period_avg)) + ' ' +\
                      html_fp_coral_text(currency) + html_fp_white(text2b) + html_fp_white(text2c) + \
                      html_fp_coral_text(per_val_max) + html_fp_white(text2d) + \
                      html_fp_coral_text(num_human_format(value_max)) + html_fp_white(text2e) + \
                      html_fp_coral_text(per_val_min) + html_fp_white(text2f) + \
                      html_fp_coral_text(num_human_format(value_min)) + html_fp_white(text2g)

        return text1_final + text2_final

    ### CHART FOR LOWER BOUND
    chart = alt.Chart(fp_period).mark_bar(size=15)\
        .encode(x=alt.X(date_col),
                y=alt.Y(cost_col),
                color=alt.value('#5CC8D7'),
                tooltip=[cost_col])\
        .interactive()

    ### CHART AND COMMENTARY
    st.altair_chart(chart,use_container_width=True)
    st.markdown(commentary(), unsafe_allow_html=True)

### FOOTPRINTS DATA STORY ONE TIME COSTS
def fp_datastory_onetime():
    ### Section Header, Spacing and Column Split
    st.header('One-Time Costs')
    st.write('Besides the predictions we made, \
              there are also one-time costs which only appeared once throughout the whole history of your dataset. \
             In this section we show you all the one-time costs and the impact they had on your costs.')

    onetime = st.session_state['one-time-costs']
    hier_col = st.session_state['hier-cols']
    cost_col = st.session_state['cost-col']
    date_col = st.session_state['datetime']
    all_cols = hier_col + [date_col] + [cost_col]
    sel_currency = st.session_state['currency']

    ### ONE-TIME KPIs
    onetime_amt = onetime[cost_col].sum()
    onetime_gb = onetime[all_cols].sort_values(by=cost_col,ascending=False).reset_index(drop=True)
    onetime_gb[cost_col + '_REAL'] = abs(onetime_gb[cost_col])

    ### ONE-TIME COSTS KPIs
    onetime_left, onetime_right = st.columns(2)
    with onetime_left:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{len(onetime):,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Detected One-Time Cost Cases</h3>", unsafe_allow_html=True)
    with onetime_right:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                num_human_format(onetime_amt)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>One-Time Costs in {}</h3>".format(st.session_state['currency']), unsafe_allow_html=True)

    ### ONE-TIME COSTS PER PERIOD
    st.title(' ')
    onetime_period = onetime.groupby(by=date_col,axis=0, as_index=False).size().rename(columns={'size':'Count'})

    ### PERIODICAL CHART
    def otc_chart():
        ### CHART FOR SIZE
        chart = alt.Chart(onetime_period).mark_bar(size=15) \
            .encode(x=alt.X(date_col),
                    y=alt.Y('Count'),
                    color=alt.value('#5CC8D7'),
                    tooltip=['Count']) \
            .interactive()

        ### CHART AND COMMENTARY
        st.markdown("<p style='text-align: center; font-size: 18px;'>{}</p>"
                    .format('One-Time Cost Cases per Period'),
                    unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True)
    otc_chart()

    ### FILTERS
    st.subheader('One-Time Costs Cases')
    otc_left, otc_right = st.columns(2)
    with otc_left:
        periods_all = ['All'] + list(onetime[date_col].str[:7].sort_values(ascending=False).unique())
        sel_period = st.selectbox('Periodical Selection', periods_all, help='Max 1.')
    with otc_right:
        otc_sort = st.selectbox('One-Time Cost Sorting',['Highest','Lowest'])
        if otc_sort == 'Highest':
            otc_sort_ind = False
        else:
            otc_sort_ind = True
    topN = st.slider('Select Top N One-Time Costs', 1, 25, 10)

    ### ONE-TIME COSTS CASES
    if sel_period == 'All':
        otc_per = onetime
    else:
        otc_per = onetime[onetime[date_col].str[:7] == sel_period]
    otc_per = otc_per.sort_values(by=cost_col,ascending=otc_sort_ind).reset_index(drop=True).head(int(topN))
    otc_per.index += 1
    st.write(otc_per[all_cols])

    ### OTC COMMENTARY
    def commentary():
        topOTC = otc_per[hier_col].agg(' - '.join, axis=1).iloc[0]
        topSum = otc_per[cost_col].iloc[0]

        ### TEXT1
        if sel_period == 'All':
            text1a = 'The {} One-Time Cost across all periods appeared in '.format(otc_sort.lower())
            text1b = otc_per[date_col].iloc[0]
        else:
            text1a = 'The highest One-Time Cost in the selected period '
            text1b = sel_period[0]

        text1c = ' appeared for '
        text1d = ' with an total amount of '
        text1e = '{} {}'.format(num_human_format(topSum),sel_currency)

        ### TEXT1 FINAL
        text1_final = html_fp_white(text1a) + html_fp_coral_text(text1b) + html_fp_white(text1c) + \
                      html_fp_coral_text(topOTC) + html_fp_white(text1d) + html_fp_coral_text(text1e) + '. '

        ### TEXT2
        text2a = 'Overall, the {}'.format(otc_sort.lower())
        text2b = 'Top {}'.format(int(topN))
        if not sel_period:
            text2c = ' One-Time Costs '
        else:
            text2c = ' One-Time Costs in the selected period '
        text2d = ' make up a total amount of '
        text2e = '{} {}'.format(num_human_format(otc_per[cost_col].sum()),sel_currency)

        ### TEXT2 FINAL
        text2_final = html_fp_white(text2a) + html_fp_coral_text(text2b) + html_fp_white(text2c) + \
                      html_fp_white(text2d) + html_fp_coral_text(text2e) + '. '

        text_final = text1_final + text2_final
        st.markdown(text_final,unsafe_allow_html=True)
    commentary()

### FOOTPRINTS DATA STORY GROWERS
def fp_datastory_change():
    fp = st.session_state['prediction']
    hier_col = st.session_state['hier-cols']
    cost_col = st.session_state['cost-col']
    date_col = st.session_state['datetime']
    all_cols = hier_col + [date_col] + [cost_col]
    gb_cols = hier_col + [date_col]

    ### SECTION HEADER
    st.header('Growers and Losers')
    st.write('The detected footprints are all unique and so is their development over the periods analyzed. \
             In this section, we are looking into the top growing and decreasing footprints in the dataset to find \
             hidden cost drivers as well as decreasing costs in certain areas.')
    st.write('Part of the analysis are only Footprints that occur in minimum 50% of the periods.')

    ### PREPARE DATA
    countPeriod = len(fp[date_col].unique()) / 2
    fp = fp[fp['FP_RATING'] == 'Okay']

    ### FILTER FOR FOOTPRINTS WITH 50% OCCURENCE
    fp_size = fp[gb_cols].groupby(by=hier_col, as_index=False).size()
    fp_size = fp_size[fp_size['size'] >= countPeriod]
    fp_period = pd.merge(fp, fp_size, on=hier_col)

    ### FILTER FOR FOOTPRINTS IN MIN AND MAX PERIOD
    fp_max = fp_period[gb_cols].groupby(by=hier_col,as_index=False).max()
    fp_min = fp_period[gb_cols].groupby(by=hier_col, as_index=False).min()

    fp_clean = fp[all_cols]
    fp_max = pd.merge(fp_clean, fp_max, on=list(fp_max.columns)).rename(columns={date_col : 'MAX_PER', cost_col : 'AMOUNT_LAST'})
    fp_min = pd.merge(fp_clean, fp_min, on=list(fp_min.columns)).rename(columns={date_col : 'MIN_PER', cost_col : 'AMOUNT_FIRST'})

    ### CALCULATE DIFFERENCE
    fp_change = pd.merge(fp_max,fp_min,on=hier_col)
    fp_change = fp_change[fp_change['AMOUNT_FIRST'] != 0]
    fp_change['CHANGE_ABS'] = fp_change['AMOUNT_LAST'] - fp_change['AMOUNT_FIRST']
    fp_change['CHANGE_REL'] = round((fp_change['CHANGE_ABS'] / fp_change['AMOUNT_FIRST']) * 100, 0)
    fp_change = pd.merge(fp_change,fp_size,on=hier_col).rename(columns={'size':'PERIODS'})

    ### HEADER AND FILTERS
    st.subheader('Top Changing Footprints')
    grow_left, grow_right = st.columns(2)
    with grow_left:
        change_type = st.selectbox('Change Types',options=['Growers','Losers'])
    with grow_right:
        abs_rel = st.selectbox('Change Type Growers',['Absolute', 'Relative'])
    topN = st.slider('Select Top N Changes', 1, 25, 10, help = 'Min 1 / Max 25')

    ### FILTER GROWER OR LOSER
    if change_type == 'Growers':
        fp_change = fp_change[fp_change['CHANGE_ABS'] > 0]
        change_sort = False
    else:
        fp_change = fp_change[fp_change['CHANGE_ABS'] < 0]
        change_sort = True

    ### FILTER ABSOLUTE OR RELATIVE
    if abs_rel == 'Absolute':
        fp_change = fp_change.sort_values(by='CHANGE_ABS', ascending=change_sort)
    else:
        fp_change = fp_change.sort_values(by='CHANGE_REL', ascending=change_sort)

    ### DATASET CLEANUP
    fp_change = fp_change.head(topN).reset_index(drop=True).drop(['MIN_PER', 'MAX_PER'], axis=1)
    fp_change.index += 1
    st.write(fp_change)

    ### TABLE COMMENTARY
    def comment_table():
        ### KPIs AND COLUMNS
        sel_currency = st.session_state['currency']

        ### TEXT 1 COMMENTARY
        text1a = 'The'
        if change_type == 'Growers':
            text1b = ' Top {} growing '.format(str(topN))
        else:
            text1b = ' Top {} decreasing '.format(str(topN))
        text1c = 'Footprints all have'
        if change_type == 'Growers':
            if abs_rel == 'Absolute':
                minChange = fp_change['CHANGE_ABS'].min()
                text1d = ' an absolute change of more than'
                text1e = '{} {}'.format(num_human_format(minChange),sel_currency)
            else:
                maxChange = fp_change['CHANGE_REL'].min()
                text1d = ' an absolute change of more than'
                text1e = '{}%'.format(int(maxChange))
        elif change_type == 'Losers':
            if abs_rel == 'Absolute':
                maxChange = fp_change['CHANGE_ABS'].max()
                text1d = ' an absolute change of more than'
                text1e = '{} {}'.format(num_human_format(maxChange), sel_currency)
            else:
                maxChange = fp_change['CHANGE_REL'].max()
                text1d = ' a relative change of more than'
                text1e = '{}%'.format(int(maxChange))

        ### FINAL TEXT1
        text1_final = html_fp_white(text1a) + html_fp_coral_text(text1b) + html_fp_white(text1c) + \
                      html_fp_white(text1d) + html_fp_coral_text(text1e) + '. '

        ### TEXT 2 COMMENTARY
        text2a = 'The top Footprint by'
        if abs_rel == 'Absolute':
            text2b = 'absolute change is '
        else:
            text2b = 'relative change is '
        text2c = fp_change[hier_col].agg(' - '.join, axis=1).iloc[0]
        if change_type == 'Growers':
            if abs_rel == 'Absolute':
                text2d = ' with an absolute increase of '
                text2e = '{} {}'.format(num_human_format(fp_change['CHANGE_ABS'].iloc[0]),sel_currency)
            else:
                text2d = ' with a relative increase of '
                text2e = str(int(fp_change['CHANGE_REL'].iloc[0])) + '%'
        else:
            if abs_rel == 'Absolute':
                text2d = ' with an absolute decrease of '
                text2e = '{} {}'.format(num_human_format(fp_change['CHANGE_ABS'].iloc[0]),sel_currency)
            else:
                text2d = ' with a relative decrease of '
                text2e = str(int(fp_change['CHANGE_REL'].iloc[0])) + '%'
        text2f = ' across'
        text2g = '{} Periods'.format(str(fp_change['PERIODS'].iloc[0]))

        ### FINAL TEXT2
        text2_final = html_fp_white(text2a) + html_fp_white(text2b) + html_fp_coral_text(text2c) + \
                      html_fp_white(text2d) + html_fp_coral_text(text2e) + html_fp_white(text2f) + \
                      html_fp_coral_text(text2g) + '.'

        ### FINAL TEXT
        final_text = text1_final + text2_final


        return st.markdown(final_text,unsafe_allow_html=True)
    comment_table()
    ### SPACING
    st.subheader('  ')

    ### DISPLAY FOOTPRINTS
    fp_change['RANK'] = fp_change.index
    fp_change['RANK'] = fp_change['RANK'].astype(str)
    fp_col = ['RANK'] + hier_col
    fp_change['FP_KEY1'] = fp_change[hier_col].agg(' - '.join, axis=1)
    fp_change['FP_KEY2'] = fp_change[fp_col].agg(' - '.join, axis=1)

    ### HEADER AND TEXT
    st.subheader('Footprint Deep Dive')
    st.write('Select the selected top footprints from above to analyze their trends.')

    ### FILTER PREDICTION TABLE
    fp_select = st.selectbox('Footprint Selection',fp_change['FP_KEY2'])
    fp_key = fp_change[fp_change['FP_KEY2'] == fp_select]['FP_KEY1'].iloc[0]
    fp['FP_KEY1'] = fp[hier_col].agg(' - '.join, axis=1)
    fp = fp[fp['FP_KEY1'] == fp_key]

    ### DISPLAY CHART
    def fp_chart():
        ### CHART FOR LOWER BOUND
        chart_low = alt.Chart(fp).mark_line(strokeDash=[1,1], point=True)\
            .encode(x=alt.X(date_col),
                    y=alt.Y('FP_LOWER_BOUND'),
                    color=alt.value('#FC776A'),
                    tooltip=[date_col,'FP_LOWER_BOUND',cost_col,'FP_UPPER_BOUND'])\
            .interactive()

        ### CHART FOR ACTUAL COSTS
        chart_act = alt.Chart(fp).mark_line(point=True)\
            .encode(x=alt.X(date_col),
                    y=alt.Y(cost_col),
                    color=alt.value('#5CC8D7'),
                    tooltip=[date_col,'FP_LOWER_BOUND',cost_col,'FP_UPPER_BOUND'])\
            .interactive()

        ### CHART FOR UPPER BOUND
        chart_up = alt.Chart(fp).mark_line(strokeDash=[1,1], point=True)\
            .encode(x=alt.X(date_col),
                    y=alt.Y('FP_UPPER_BOUND'),
                    color=alt.value('#FC776A'),
                    tooltip=[date_col,'FP_LOWER_BOUND',cost_col,'FP_UPPER_BOUND'])\
            .interactive()

        ### MERGE ALL CHARTS
        chart = alt.layer(chart_low, chart_act, chart_up)
        return st.altair_chart(chart, use_container_width=True)
    ### HEADER
    fp_chart()


############################ OUTLIER DETECTION FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_outliers_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Outlier Detection')
    with titleright:
        st.image('images/fp-logo.png')

### FOOTPRINTS WELCOMING TEXT
def fp_outliers_welcome():
    st.subheader('Unveil the Unseen!')
    st.markdown("In the Outlier Detection, the Footprints AI will look for any kinds of deviations coming from your data. \
                There are several kinds of outliers, differentiating in type and amount. This section will enable you to \
                completely drill down to the raw data you were initally inputting to gain deep insights and understand \
                where the outliers are coming from.")

### FOOTPRINTS OUTLIER KPIs
def fp_outliers_kpis():
    st.header('Outlier KPIs')
    st.write('To get started, here is an overview of some of the most critical KPIs for the Outlier Analysis.')

    ### KPI GENERATION
    outlier_high = len(st.session_state['prediction'][st.session_state['prediction']['FP_RATING'] == 'Too High'])
    outlier_low = len(st.session_state['prediction'][st.session_state['prediction']['FP_RATING'] == 'Too Low'])
    deviation_sum = st.session_state['prediction']['FP_DEV_ABS'].sum()

    # KPI Boxes in 4 columns
    kpileft, kpimidleft, kpimidright, kpiright = st.columns(4)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{len(st.session_state["prediction"]):,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Total Predictions Made</h3>".format(st.session_state['currency']),unsafe_allow_html=True)
    with kpimidleft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{outlier_high:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Detected Outliers Too High</h3>", unsafe_allow_html=True)
    with kpimidright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                f'{outlier_low:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Detected Outliers Too Low</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #FC776A; border-radius: 8px; color: #FC776A;'>{}</h1>".format(
                num_human_format(deviation_sum)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Expected Deviation in {}</h3>".format(st.session_state['currency']), unsafe_allow_html=True)

### FOOTPRINTS OUTLIER PER PERIOD
def fp_outliers_periods():
    st.header('Outliers by Period')
    st.write('View when how many outliers appeared in each analyzed period by the outlier count and expected deviation amount.')

    sel_datetime = st.session_state['datetime']

    # Create Table for Outliers
    outlier_table = st.session_state['prediction'][(st.session_state['prediction']['FP_RATING'] == 'Too Low') | (st.session_state['prediction']['FP_RATING'] == 'Too High')]
    outlier_table[sel_datetime] = outlier_table[sel_datetime].str[:7]

    # Count per Outlier Rating per Period
    outlier_cnt = outlier_table.groupby(by=[sel_datetime,'FP_RATING'], axis=0, as_index=False).size()
    outlier_amt = outlier_table.groupby(by=[sel_datetime,'FP_RATING'], axis=0, as_index=False).sum('FP_DEV_ABS')[[sel_datetime,'FP_RATING','FP_DEV_ABS']]

    ### FILTER FOR PLOT
    outl_kind = st.selectbox('Periodical Outlier Filter',options=['By Amount','By Count'])
    if outl_kind == 'By Amount':
        st.subheader('Outlier Amount by Period')
        st.subheader('  ')
    else:
        st.subheader('Outlier Count by Period')
        st.subheader('  ')

    ### PERIODICAL CHART
    def outl_chart():
        if outl_kind == 'By Amount':
            ### CHART FOR AMOUNT
            chart = alt.Chart(outlier_amt).mark_bar().encode(
                x=alt.X('FP_RATING:O', title=None),
                y=alt.Y('FP_DEV_ABS:Q', title=None),
                column=alt.Column(sel_datetime, title=None),
                color=alt.Color('FP_RATING',scale=alt.Scale(range=['#FC776A', '#5CC8D7'])),
                tooltip=[sel_datetime,'FP_DEV_ABS']) \
            .configure_view(strokeWidth=0.0) \
            .interactive()
        else:
            ### CHART FOR SIZE
            chart = alt.Chart(outlier_cnt).mark_bar().encode(
                        x='FP_RATING:O',
                        y='size:Q',
                        column=alt.Column(sel_datetime, title=None),
                        color=alt.Color('FP_RATING', scale=alt.Scale(range=['#FC776A','#5CC8D7'])),
                        tooltip=[sel_datetime,'size']) \
                .configure_view(strokeWidth=0.0) \
                .interactive()

        ### CHART AND COMMENTARY
        st.altair_chart(chart)
    outl_chart()

### FOOTPRINTS OUTLIER PER HIERARCHY
def fp_outliers_hierarchy():

    st.header('Outliers by Hierarchy')
    st.write('Find the origin of outliers by your hierarchy based on Deviation Amount or Outlier Count.')

    prediction = st.session_state['prediction']
    sel_hierarchy = st.session_state['hier-cols']
    sel_costcol = st.session_state['cost-col']

    ### SELECTION BOXES
    left, right = st.columns(2)
    with left:
        sel_hierarchy = st.multiselect('Select Hierarchy Columns', sel_hierarchy)
    with right:
        sel_type = st.selectbox('Sort Outliers by',['Deviation Amount','Outlier Count'])

    ### GET TOP N SLIDER
    topN = st.slider('Select Top N Outliers', 1, 25, 10,help='Maximum Top N is 25.')

    ### GENERATE THE TABLE
    if not sel_hierarchy:
        st.info('Please select a hierarchy column.')
    else:
        ### CALCULATE DEVIATION AMOUNT
        outl_amt = prediction.groupby(sel_hierarchy,as_index=False).sum()[sel_hierarchy + [sel_costcol]]
        outl_amt = outl_amt.rename(columns={sel_costcol : 'Deviation Amount'}).reset_index(drop=True)

        ### CALCULATE OUTLIER COUNT
        outl_cnt = prediction.groupby(sel_hierarchy, as_index=False).size()[sel_hierarchy + ['size']]
        outl_cnt = outl_cnt.rename(columns={'size': 'Outlier Count'}).reset_index(drop=True)

        ### FINALIZE TABLE
        hier_table = pd.merge(outl_amt,outl_cnt,how='outer',on=sel_hierarchy)
        if sel_type == 'Deviation Amount':
            hier_table = hier_table.sort_values(by='Deviation Amount',axis=0,ascending=False)[:topN]
            hier_table['Deviation Amount'] = hier_table.apply(lambda row: num_human_format(row['Deviation Amount']), axis=1)
            hier_table = hier_table.reset_index(drop=True)
            hier_table.index += 1
        else:
            hier_table = hier_table.sort_values(by='Outlier Count', axis=0, ascending=False)[:topN]
            hier_table['Deviation Amount'] = hier_table.apply(lambda row: num_human_format(row['Deviation Amount']), axis=1)
            hier_table = hier_table.reset_index(drop=True)
            hier_table.index += 1

        if len(hier_table) < topN:
            st.info('Selection has less elements than Top N selection (Max = ' + str(len(outl_cnt)) + ').')

        st.write(hier_table)

### FOOTPRINTS TOP OUTLIERS
def fp_outliers_top_outliers():
    st.header('Top Single Outliers by Hierarchy')
    st.write('Check the Top Too High Outliers in the selected period.')

    sel_hierarchy = st.session_state['hier-cols']
    sel_costcol = st.session_state['cost-col']
    sel_datetime = st.session_state['datetime']

    periods_all = st.session_state['prediction'][st.session_state['datetime']].str[:7].sort_values(ascending=False).unique()
    outl_left, outl_right = st.columns(2)
    with outl_left:
        sel_period = st.selectbox('Periodical Selection',periods_all,help='Select Period you would like to analyze closer.')
        st.session_state['outlier_period_sel'] = sel_period
    with outl_right:
        sel_devtype = st.selectbox('Deviation Type',['All','Too Low','Too High'],help='Selection between All, Too High or Too Low deviations.')


    ### SLIDER FOR TOP N VALUES
    topN = st.slider('Select Top Single Outliers',1,25,value=10,help='Maximum Top N is 25.')

    ### FILTER DEVIATION TYPES
    if sel_devtype != 'All':
        outlier_table = st.session_state['prediction'][st.session_state['prediction']['FP_RATING'] == sel_devtype]
    else:
        outlier_table = st.session_state['prediction'][st.session_state['prediction']['FP_RATING'] != 'Okay']

    outlier_table[sel_datetime] = outlier_table[sel_datetime].str[:7]

    ### FILTER TABLE AND SORT BY ABSOLUTE DEVIATION
    outlier_table = outlier_table[outlier_table[sel_datetime] == sel_period]
    outlier_table = outlier_table.sort_values(by='FP_DEV_ABS', ascending=False).reset_index(drop=True)

    ### SELECT COLUMNS AND FILTER FOR TOPN
    outlier_table['RANK'] = outlier_table.index + 1
    outlier_cols = ['RANK'] + sel_hierarchy + ['FP_RATING','FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_DEV_ABS']
    outlier_table = outlier_table[outlier_cols][:topN]
    outlier_table.index += 1

    ### REFORMATTING NUMERICAL COLUMNS
    for col in ['FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_DEV_ABS']:
        outlier_table[col] = outlier_table.apply(lambda row: num_human_format(row[col]), axis=1)

    ### HINT THAT N IS BIGGER THAN TABLE LENGTH
    if topN > len(outlier_table):
        st.info('The selected N is higher than available the available results.')

    ### STOP IF NO RESULTS
    if len(outlier_table) == 0:
        st.info('No results in the outlier table. Please change the filters.')
        check_indicator = False
    else:
        st.write(outlier_table)
        check_indicator = True

    return outlier_table, check_indicator

### FOOTPRINTS OUTLIER INVESTIGATION
def fp_outliers_footprints():
    ### HEADER
    st.header('Footprint Deep Dive')
    st.write('Check the Top Too High Outliers in the selected period.')

    sel_hierarchy = st.session_state['hier-cols']
    sel_costcol = st.session_state['cost-col']
    sel_datetime = st.session_state['datetime']
    sel_period = st.session_state['outlier_period_sel']

    ### CALCULATE KEY COLUMNS TO CROSS-FILTER
    filter_col = ['RANK'] + sel_hierarchy
    outlier_table['RANK'] = outlier_table['RANK'].astype(str)
    outlier_table['FP_KEY1'] = outlier_table[filter_col].agg(' - '.join, axis=1)
    outlier_table['FP_KEY2'] = outlier_table[sel_hierarchy].agg(' - '.join, axis=1)

    ### FOOTPRINTS SELECTION
    sel_fp = st.selectbox('Select Footprint',outlier_table['FP_KEY1'])
    outlier_tab = outlier_table[outlier_table['FP_KEY1'] == sel_fp]

    ### FILTER TRANSACTIONAL TABLE
    footprint_name = outlier_tab['FP_KEY2'].iloc[0]
    st.session_state['prediction']['FP_KEY1'] = st.session_state['prediction'][sel_hierarchy].agg(' - '.join, axis=1)
    raw_filter = st.session_state['prediction'][st.session_state['prediction']['FP_KEY1'] == footprint_name]

    ### CREATE CHART DATA
    st.subheader('Footprint Development')
    st.subheader(' ')
    filter_col = sel_hierarchy + [sel_datetime,'FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_RATING','FP_DEV_ABS']
    footprint = raw_filter[filter_col]
    footprint[sel_datetime] = footprint[sel_datetime].str[:7]

    ### CHART FOR LOWER BOUND
    chart_low = alt.Chart(footprint).mark_line(strokeDash=[1,1], point=True)\
        .encode(x=alt.X(st.session_state['datetime']),
                y=alt.Y('FP_LOWER_BOUND'),
                color=alt.value('#FC776A'),
                tooltip=[sel_datetime,'FP_RATING','FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_DEV_ABS'])\
        .interactive()

    ### CHART FOR ACTUAL COSTS
    chart_act = alt.Chart(footprint).mark_line(point=True)\
        .encode(x=alt.X(st.session_state['datetime']),
                y=alt.Y(sel_costcol),
                color=alt.value('#5CC8D7'),
                tooltip=[sel_datetime,'FP_RATING','FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_DEV_ABS'])\
        .interactive()

    ### CHART FOR UPPER BOUND
    chart_up = alt.Chart(footprint).mark_line(strokeDash=[1,1], point=True)\
        .encode(x=alt.X(st.session_state['datetime']),
                y=alt.Y('FP_UPPER_BOUND'),
                color=alt.value('#FC776A'),
                tooltip=[sel_datetime,'FP_RATING','FP_LOWER_BOUND',sel_costcol,'FP_UPPER_BOUND','FP_DEV_ABS'])\
        .interactive()

    ### MERGE ALL CHARTS
    chart = alt.layer(chart_low, chart_act, chart_up)
    st.altair_chart(chart, use_container_width=True)

    ### FOOTPRINT COMMENTARY
    def commentary():

        ### COMMENTARY KPIs
        period_count = len(footprint)
        fp_name = footprint_name
        outlier_count = len(footprint[footprint['FP_RATING'] != 'Okay'])
        curr_per_outl = footprint[footprint[sel_datetime] == sel_period]['FP_RATING'].iloc[0]
        curr_costs = footprint[footprint[sel_datetime] == sel_period][sel_costcol].iloc[0]
        curr_dev = footprint[footprint[sel_datetime] == sel_period]['FP_DEV_ABS'].iloc[0]
        outl_quota = str(round((outlier_count / period_count) * 100,2)) + '%'

        ### TEXT1
        text1a = 'The selected footprint '
        text1b = ' shows for the selected period of '
        text1c = ' an outlier with a '
        text1d = ' indicator.'

        text1 = html_fp_white(text1a) + html_fp_coral_text(fp_name) + html_fp_white(text1b) + html_fp_coral_text(sel_period) + \
                html_fp_white(text1c) + html_fp_coral_text(curr_per_outl) + html_fp_white(text1d)

        ### TEXT2
        text2a = ' The actual amount of '
        text2b = ' deviates '
        text2c = ' from the initially expected amount.'

        text2 = html_fp_white(text2a) + html_fp_coral_text(num_human_format(curr_costs)) + ' ' + html_fp_coral_text(st.session_state['currency']) + \
                html_fp_white(text2b) + html_fp_coral_text(num_human_format(curr_dev)) + ' ' + html_fp_coral_text(st.session_state['currency']) + html_fp_white(text2c)

        ### TEXT3
        text3a = 'Along the '
        text3b = ' different periods, the footprint showed '
        text3c = ' outliers which equals to an outlier quota of '
        text3d = '.'

        text3 = html_fp_white(text3a) + html_fp_coral_kpi(period_count) + html_fp_white(text3b) + \
                html_fp_coral_kpi(outlier_count) + html_fp_white(text3c) + html_fp_coral_text(outl_quota) + \
                html_fp_white(text3d)

        ### DISPLAY FINAL TEXT
        final_text = text1 + text2 + text3
        return st.markdown(final_text,unsafe_allow_html=True)
    commentary()

    ### TRANSACTIONAL BREAKDOWN
    st.subheader('  ')
    st.subheader('Footprint Transactional Breakdown')
    st.markdown('In this section is a further breakdown of the data of the \
                 selected footprint based on the original input data.')

    ### FILTER RAW DATA
    sel_period = str(sel_period) + '-01'
    raw_data = st.session_state['raw-data']
    raw_data['FP_NAME'] = raw_data[sel_hierarchy].agg(' - '.join, axis=1)
    raw_data = raw_data[(raw_data['FP_NAME'] == footprint_name) & (raw_data[sel_datetime] == sel_period)]
    raw_data = raw_data.sort_values(by=sel_costcol,ascending=False).drop('FP_NAME',axis=1).reset_index(drop=True)

    ### FINALIZE RAW DATA TABLE
    raw_data.index += 1
    st.write(raw_data)


################################ FEEDBACK PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PAGE HEADER
def fp_feedback_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('WebApp Feedback')
    with titleright:
        st.image('images/fp-logo.png') # FROM GITHUB

### FOOTPRINTS WELCOMING TEXT
def fp_feedback_welcome():
    st.subheader('Share your experiences!')
    st.markdown("Footprints grows with and because of you. Therefore, we are constantly looking for feedback and try to understand how \
                 you experienced the Footprints journey in the WebApp. Below, you find a few questions about each page \
                to share your experiences with us.")

    # TEXT 1 GENERATION
    text1a = 'The rating goes from '
    text1b = '1 as the lowest '
    text1c = 'to '
    text1d = '5 as the highest'
    # COMBINE ALL TEXTs TOGETHER
    final = html_fp_white(text1a) + html_fp_blue_text(text1b) + html_fp_white(text1c) + html_fp_coral_text(text1d) + '.'
    st.markdown(final, unsafe_allow_html=True)

### FEEDBACK OVERALL EXPERIENCE
def fp_feedback_form():
    ### CREATE FEEDBACK FORM
    st.subheader('Footprints Feedback Form')
    with st.form('fp-feedback'):
        ### FEEDBACK OVERALL
        def feedback_ovr():
            st.subheader('Overall Experience')
            fb1_rat = st.slider('Rate your overall experience',1,5,3)
            fb1_com = st.text_input('Additional Comments - Overall Experience')

            return fb1_rat,fb1_com
        ### FEEDBACK PAGES
        def feedback_page():
            st.subheader('Page Feedback')
            st.markdown('##### Get Started Experience')

            feedback_left, feedback_right = st.columns(2)
            with feedback_left:
                fb2_rat = st.slider(' ',1,5,3)
            with feedback_right:
                fb2_com = st.text_area('Additional Comments - Get Started Experience')

            st.markdown('##### Data Input')
            feedback_left, feedback_right = st.columns(2)
            with feedback_left:
                fb3_rat = st.slider('  ',1,5,3)
            with feedback_right:
                fb3_com = st.text_area('Additional Comments - Data Input')

            st.markdown('##### Data Story')
            feedback_left, feedback_right = st.columns(2)
            with feedback_left:
                fb4_rat = st.slider('   ',1,5,3)
            with feedback_right:
                fb4_com = st.text_area('Additional Comments - Data Story')

            st.markdown('##### Outlier Detection')
            feedback_left, feedback_right = st.columns(2)
            with feedback_left:
                fb5_rat = st.slider('    ',1,5,3)
            with feedback_right:
                fb5_com = st.text_area('Additional Comments - Outlier Detection')

            return fb2_rat,fb2_com,fb3_rat,fb3_com,fb4_rat,fb4_com,fb5_rat,fb5_com
        ### FEEDBACK FINAL THOUGHTS
        def feedback_final():
            st.subheader('Final Thoughts')
            fb6_com = st.text_input('Do you see Footprints as a useful tool for your organization?')
            fb7_com = st.text_input('Is there any feature you would like to see being added?')

            return fb6_com,fb7_com

        ### FEEDBACK OVR DISPLAY
        fb_ovr_output = feedback_ovr()
        ### SPACING
        st.markdown('---')
        ### FEEDBACK PAGE DISPLAY
        fb_exp_output = feedback_page()
        ### SPACING
        st.markdown('---')
        ### FEEDBACK FINAL
        fb_fin_output = feedback_final()
        ### SPACING
        st.markdown('---')
        ### FEEDBACK MAIL
        st.subheader('Submit your Feedback')
        try:
            mail = st.text_input('Your email address',value=st.session_state['EMAIL'])
        except KeyError:
            mail = st.text_input('Your email address')

        ### CREATE FEEDBACK TABLE
        feedback = list(fb_ovr_output) + list(fb_exp_output) + list(fb_fin_output)
        feedback_df = pd.DataFrame(feedback).transpose()
        ### FINALIZE FEEDBACK TABLE
        feedback_df.columns = ['Q1_OVR_RATING', 'Q1_OVR_COMMENT', 'Q2_LOGIN_RATING', 'Q2_LOGIN_COMMENT',
                               'Q3_INPUT_RATING', 'Q3_INPUT_COMMENT', 'Q4_STORY_RATING', 'Q4_STORY_COMMENT',
                               'Q5_OUTLIER_RATING', 'Q5_OUTLIER_COMMENT', 'Q6_USEFUL_TOOL', 'Q7_ADDITIONAL_FEATURES']
        feedback_df['FEEDBACK_MAIL'] = mail
        feedback_df['FEEDBACK_SUBMISSION'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_df['SESSION_ID'] = st.session_state['SESSION_ID']

        ### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            ### CHECK MAIL FORMAT
            if not mail:
                st.error('Please enter an email address!')
            elif '@' not in mail:
                st.error('Please enter a valid email address.')
            elif '.' not in mail:
                st.error('Please enter a valid email address.')

            ### WRITE DATA TO CSV
            try:
                type = 'Feedback'
                feedback_df.to_csv('/Users/kevin/Google Drive/.shortcut-targets-by-id/1pkEbWCt9mdIhGXKn6vnn6IIbA3LUbWuI/Footprints Start-Up /Data Repository/fp-user-feedback.csv', mode='a', index=False, header=False)
                st.balloons()
                st.success('Feedback submitted. Thank you very much! ❤️')
            except:
                type = 'Feedback'
                fp_app_notification(type,feedback_df)
                st.balloons()
                st.success('Feedback submitted. Thank you very much! ❤️')


################################# WELCOME PAGE FUNCTIONS ##########
###################################################################

### FOOTPRINTS PREVIEW HEADER
def fp_preview_header():
    ### INTRODUCTION TEXT
    titleleft, titlemid, titleright = st.columns(3)
    with titleleft:
        st.title('Footprints Outlook')
    with titleright:
        st.image('images/fp-logo.png') # FROM GITHUB

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
        text_final = html_fp_white(text1a) + html_fp_coral_text(text1b) + html_fp_white(text1c) + \
                     html_fp_coral_text(text1d) + ', '+ html_fp_coral_text(text1e) + html_fp_white(text1f) + \
                     html_fp_coral_text(text1g) + '. ' + html_fp_white(text1h)
        return st.markdown(text_final, unsafe_allow_html=True)

    ### FUNCTION
    functionalities()
    ### SPACING
    st.subheader(' ')
    ### SCREENSHOT
    st.image('images/figma/page1.png') # FROM GITHUB
    ### CAPTION
    st.markdown("<p style='text-align: center; font-size: 14px;'>{}</p>"
                .format('Footprints WebApp starting page with functions such as New Footprints and Job Status Overview.'), unsafe_allow_html=True)

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
        text_final = html_fp_white(text1a) + html_fp_coral_text(text1b) + html_fp_white(text1c) + \
                     html_fp_coral_text(text1d) + html_fp_white(text1e) + html_fp_coral_text(text1f) + \
                     html_fp_white(text1g)
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
        text_final = html_fp_white(text1a) + html_fp_coral_text(text1b) + '. ' + html_fp_white(text1c) + \
                     html_fp_coral_text(text1d) + ', ' + html_fp_coral_text(text1e) + html_fp_white(text1f) + \
                     html_fp_coral_text(text1g) + '. ' + html_fp_white(text1h) + html_fp_coral_text(text1i) + '.'
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


########################################### RUN APP FUNCTIONS #############################################
###########################################################################################################

### RUN APP SETTINGS
fp_app_settings()
### RUN SIDEBAR
page_select = fp_app_sidebar()
### PAGE SELECT FUNCTION
if page_select == 'Home':
    ### HEADER
    fp_home_header()
    ### WElCOME
    fp_home_welcome()
    ### SPACING
    st.markdown('---')
    ### APP CONTENT
    fp_home_content()
    ### SPACING
    st.markdown('---')
    ### FAQ
    fp_home_faq()
elif page_select == 'Get Started':
    ### HEADER
    fp_login_header()
    ### WElCOME
    fp_login_welcome()
    try:
        if st.session_state['LOGIN'] == True:
            st.info('You already shared your mail with us. In case you want to start over click on the Start Again button in the sidebar.')
        elif st.session_state['RESTART'] == True:
            fp_login_submit()
    except KeyError:
        fp_login_submit()
elif page_select == 'Data Input':
    # HEADER
    fp_input_header()
    # WELCOME
    fp_input_welcome()
    try:
        login_check = st.session_state['LOGIN']
    except KeyError:
        st.info('Please sign in in the Get Started page before you can upload data.')
    else:
        if st.session_state['LOGIN'] == False:
            st.info('Please share you mail in the Get Started page before you can upload data.')
        else:
            # SPACING
            st.markdown('---')
            # DATA UPLOAD
            cost_data, file_uploaded = fp_input_upload()
            # DATA HIERARCHY
            if file_uploaded == True:
                st.markdown('---')
                submit_status, sel_costcol, sel_datetime, sel_hierarchy, sel_currency, hier_status = fp_input_hierarchy()
                pred_col = [sel_datetime] + sel_hierarchy
            # ML TRANSFORMATION
            if hier_status == True:
                st.markdown('---')
                transform_status, cost_pred, cost_onetime, loop_list = fp_input_ml_transformation()
            # ML PREDICTION
            if transform_status == True:
                if st.button('Start Prediction'):
                    pred_status, runtime, final_pred, norm_set = fp_input_ml_prediction()
                else:
                    pred_status = False
            # ML CONSTRUCT
            if pred_status == True:
                st.write()
                st.markdown('---')
                prediction = fp_input_ml_construct(norm_set)
                st.session_state['prediction'] = prediction
elif page_select == 'Data Story':
    try:
        ### FP HEADER
        fp_datastory_header()
        ### FP WELCOME
        fp_datastory_welcome()
        ### FP PREDICTION CHECK
        fp_app_predcheck()
        ### SPACING
        st.markdown('---')
        ### FP OVERALL RESULT
        fp_datastory_kpis()
        ### SPACING
        st.markdown('---')
        ### FP COST DRIVERS
        fp_datastory_costdriver()
        ### SPACING
        st.markdown('---')
        ### FP PERIODICAL ANALYSIS
        fp_datastory_periods()
        ### SPACING
        st.markdown('---')
        ### FP ONE-TIME COSTS
        fp_datastory_onetime()
        ### SPACING
        st.markdown('---')
        ### FP CHANGES
        fp_datastory_change()
    except KeyError:
        st.info('No footprints available yet. Please run through the Data Input page and then check the Data Story again.')
elif page_select == 'Outlier Detection':
    try:
        ### FP HEADER
        fp_outliers_header()
        ### FP WELCOME
        fp_outliers_welcome()
        ### FP PREDICTION CHECK
        fp_app_predcheck()
        ### SPACING
        st.markdown('---')
        # OUTLIER KPIs
        fp_outliers_kpis()
        st.markdown('---')
        # OUTLIER PERIOD VIEW
        fp_outliers_periods()
        st.markdown('---')
        # OUTLIER HIERARCHY
        fp_outliers_hierarchy()
        st.markdown('---')
        # TOP OUTLIERS
        outlier_table, check_indicator = fp_outliers_top_outliers()
        # FOOTPRINT INVESTIGATION
        if check_indicator == False:
            pass
        else:
            fp_outliers_footprints()
    except KeyError:
        st.info('No footprints available yet. Please run through the Data Input page and then check the Outlier Detection again.')
elif page_select == 'Feedback':
    ### FP HEADER
    fp_feedback_header()
    ### WElCOME
    fp_feedback_welcome()
    try:
        check_login = st.session_state['LOGIN']
    except KeyError:
        st.title(' ')
        st.info('Please share you mail on the Get Started page first before you can give us feedback.')
    else:
        if st.session_state['LOGIN'] == False:
            ### SPACING
            st.subheader(' ')
            ### INFO
            st.info('Please share you mail in the Get Started page before you can upload data.')
        else:
            ### SPACING
            st.subheader(' ')
            ### OVERALL EXPERIENCE
            fp_feedback_form()
elif page_select == 'Outlook':
    ### PREVIEW HEADER
    fp_preview_header()
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
### FOOTER
fp_app_footer()