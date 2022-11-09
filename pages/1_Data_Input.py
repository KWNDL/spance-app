# External Libraries
import pandas as pd
import numpy as np
import datetime
import time
from sklearn.ensemble import GradientBoostingRegressor
# Internal libraries
from app_style import *


# Session State Variables created:
# - sp_input_df_rawdata               Raw Data Input, either upload or sample
# - sp_input_df_prediction            Prediction Output after ML
# - sp_input_df_onetimecost           One Time cost detected before ML
# - sp_input_df_outlier               Prediction Output after ML not within the band
# - sp_input_selection_granularity    What time granularity has been selected
# - sp_input_selection_currency       What currency has been selected
# - sp_input_predcol_cost             Prediction Column for Cost
# - sp_input_predcol_datetime         Prediction Column for Datetime
# - sp_input_predcol_hierarchy        Prediction Column for Hierarchy
# - sp_input_status_hierarchy         true if Hierarchy has been confirmed and created
# - sp_input_status_prediction        true if Prediction has been run


# Page Settings
page_settings('Data Input - Spance')
# Sidebar Logo
sidebar_logo('images/sp_logo_header.png')
# Page Header
header('Data Input')


# Welcoming Text
def input_welcome():
    st.subheader('With the Power of AI!')
    st.markdown("Now we're ready to experience a whole new experience of AI and Machine Learning to get never seen insights \
                 from your data. On this page, simply upload your cost data files in CSV or Excel format or pick the \
                 provided sample data. Then, you select the cost column, a data column and any \
                 kind of hierarchy within your data to be analyzed.")


# Data Upload
def input_upload():
    ### FILE UPLOAD
    st.subheader('Uploading Data')
    st.markdown("Let's start with data. Select either our sample data or your own data. In case you chose your own example, the maximum \
                 size is 200MB.")
    # Select Sample Data or Upload Data
    upload_select = st.selectbox('Select the data source', ['Upload Data', 'Sample Data'])

    ### FUNCTION FOR FILE SELECTION: EITHER SAMPLE OR OWN DATA
    def file_selection(upload_select):
        if upload_select == 'Sample Data':
            cost_data = pd.read_csv('data/fp-data.csv')
            cost_data = pd.DataFrame(cost_data)
            st.session_state['sp_input_df_rawdata'] = cost_data
            time.sleep(0.5)
            st.success('Sample load successful!')
            return cost_data
        elif upload_select == 'Upload Data':
            file_upload = st.file_uploader("Upload your data", type=['csv'])
            if file_upload != None:
                # Uploaded cost data
                cost_data = pd.read_csv(file_upload)
                cost_data = pd.DataFrame(cost_data)
                st.session_state['sp_input_df_rawdata'] = cost_data
                time.sleep(0.5)
                st.success('Upload successful!')
                return cost_data
            else:
                # If no upload then footer and stop
                footer()
                st.stop()

    # Display the cost data
    cost_data = file_selection(upload_select)
    st.subheader('Data Preview')
    # Select the first 1000 rows
    st.markdown('Preview of the first 1000 rows.')
    cost_data_display = cost_data.head(1000).reset_index(drop=True)  # .sample(frac=1)
    cost_data_display.index += 1
    st.dataframe(cost_data_display)

    ### DATA ROW AND COLUMN COUNT COMMENTARY
    def input_commentary():
        # ROW AND COLUMN COUNT KPIs
        cost_data_rows = len(cost_data)
        cost_data_cols = len(cost_data.columns)

        # TEXT FOR COMMENTARY
        text1a = 'The data has'
        text1b = ' rows '
        text1c = 'and'
        text1d = ' columns'

        # FINAL TEXT
        text_final = html_text(text1a) + html_highlight_text(cost_data_rows) + \
                     html_highlight_text(text1b) + html_text(text1c) + \
                     html_highlight_kpi(cost_data_cols) + html_highlight_text(text1d) + '.'
        return text_final

    # Display row and column count
    st.markdown(input_commentary(), unsafe_allow_html=True)

    # Expander Box for Sample Data
    st.subheader('  ')
    if upload_select == 'Sample Data':
        with st.expander('What do the columns stand for?'):
            st.markdown("""
                        The sample data represents a **fictional company** with multiple sites across different
                        countries and sites. The dataset contains data on a **transactional level** \
                        which means that every single row shows one single spending.

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
                        - **Company:** Sample Company Name
                        - **Company Site:** Location of Company
                        - **Unit and Sub Unit:** Business Organizational Structure
                        """)

    ### FINAL CHECK THAT FILE UPLOADED, THEN RETURN TABLE
    file_uploaded = True
    return cost_data, file_uploaded


### Spance HIERARCHY SELECTION
def input_hierarchy(data):
    ### OPENING TEXT
    st.subheader('Hierarchy Selection')
    st.markdown("""
                Next, you need to select three types of columns::
                - **Cost Column:** Numerical Column that contains cost amount
                - **Datetime Column:** Column that indicates the time when the spending has been made
                - **Multiple Hierarchy Columns:** Combination of columns for cost insights and patterns
                """)
    st.subheader('  ')

    # Detect Date Columns
    for c in data.columns:
        if (data[c].dtype == float) | (data[c].dtype == int):
            pass
        else:
            try:
                data[c] = pd.to_datetime(data[c])
            except:
                pass

    # create file type lists
    intCols = list(data.select_dtypes(include=int).columns)
    fltCols = list(data.select_dtypes(include=float).columns)
    datCols = list(data.select_dtypes(include=[np.datetime64]).columns)
    strCols = list(data.select_dtypes(include=[object]).columns)
    numCols = fltCols + intCols
    catCols = sorted(intCols + strCols)

    ### FORM HIERARCHY SELECTION
    with st.form('Dimension Selection'):
        ### SELECT COST COLUMN AND CURRENCY
        st.markdown('Select Cost Column and the respective currency.')
        left_col, right_col = st.columns(2)
        with left_col:
            sel_costcol = st.selectbox('Cost Column', options=numCols)
            st.session_state['sp_input_predcol_cost'] = sel_costcol
        with right_col:
            sel_currency = st.selectbox('Currency', ['EUR', 'USD', 'AUD', 'SGD', 'MYR', 'CNY'])
            st.session_state['sp_input_selection_currency'] = sel_currency

        ### SELECT DATETIME COLUMN AND GRANULARITY
        st.markdown('Select Datetime column.')

        left_col, right_col = st.columns(2)
        with left_col:
            sel_datetime = st.selectbox('Datetime Column', options=datCols)
            st.session_state['sp_input_predcol_datetime'] = sel_datetime
        with right_col:
            sel_granularity = st.selectbox('Time Granularity', ['Month', 'Week', 'Day'],
                                           help='Currently inactive.')
            st.session_state['sp_input_selection_granularity'] = sel_granularity

        # Select Hierarchy columns
        st.markdown(
            'Next, select dimension columns in order to specify on with level \
             you want to create your cost predictions. A particular order is not required.')
        sel_hierarchy = st.multiselect('Dimension Columns', options=catCols, help='No maximum hierarchies.')
        st.session_state['sp_input_predcol_hierarchy'] = sel_hierarchy

        # Submit the Hierarchy
        submitted = st.form_submit_button("Confirm Dimensions")
        if submitted:
            if len(sel_hierarchy) == 0:
                st.error('No hierarchy column selected.')
                st.stop()
            ### HIER STATUS
            st.session_state['sp_input_status_hierarchy'] = True

            ### DISPLAY HIERARCHY OVERVIEW
            def hierarchy_overview():
                ### INTRODUCTION TEXT
                st.subheader('Dimension Overview')
                st.markdown('Now it is about to time to run the data transformation to bring the data in shape according to your selected values. \
                                          Down below you see an overview of your selected hierarchies.')

                ### FIND HIERARCHY COLUMN HIERARCHY
                hier_name = []
                hier_count = []

                for col in sel_hierarchy:
                    hier_name.append(col)
                    hier_count.append(len(data[col].unique()))

                    hier_level = pd.DataFrame({'HIERARCHY_NAME': hier_name, 'HIERARCHY_VALUES': hier_count}) \
                        .sort_values('HIERARCHY_VALUES', ascending=True).reset_index()
                    hier_level['index'] = hier_level.index
                    hier_level['index'] += 1
                    hier_level = hier_level.rename(columns={'index': 'HIERARCHY_LEVEL'})
                    hier_level.index += 1
                    st.session_state['sp_input_selection_hier_level'] = hier_level

                ### WRITE HIERARCHY TABLE
                st.write(hier_level)

                ### CREATE HIERARCHY COMMENTARY
                def commentary():
                    ### HIERARCHY KPIs
                    loop_list = data.groupby(sel_hierarchy, as_index=False).size() \
                        .drop('size', axis=1).reset_index()
                    footprint_count = len(loop_list)
                    footprint_hier = len(sel_hierarchy)

                    ### COMMENTARIES
                    text1a = 'A total of'
                    text1b = ' dimensions'
                    text1c = ' based on'
                    if len(sel_hierarchy) == 1:
                        text1d = ' Hierarchy'
                    else:
                        text1d = ' columns'
                    text1e = ' will be analyzed.'

                    ### CREATE FINAL TEXT
                    final_text = html_text(text1a) + html_highlight_text(footprint_count) + \
                                 html_highlight_text(text1b) + html_text(text1c) + \
                                 html_highlight_text(footprint_hier) + html_highlight_text(text1d) + \
                                 html_text(text1e)
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
        hier_status = st.session_state['sp_input_status_hierarchy']
        return submit_status, sel_costcol, sel_datetime, sel_hierarchy, sel_currency, hier_status
    else:
        footer()
        st.stop()


### Spance DATA TRANSFORMATION
def input_ml_transformation():
    ### INTRODUCTION TEXT
    st.subheader('Analyzing your Data')
    st.markdown('We are now ready to analyze your data based on the selected hierarchy.')

    ### DATA PREPARATION
    cost_data['spance_row_count'] = 1
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
    loop_list = loop_list.rename(columns={'index': 'spance_loop_id'})
    loop_list['spance_loop_id'] += 1

    # GroupBy Multi Entries by Hierarchy + Month, Calculate Total Costs and Bookings, then add Loop ID
    cost_pred = cost_pred.groupby(by=pred_col, as_index=False)[sel_costcol,'spance_row_count'].sum()
    cost_pred = pd.merge(cost_pred, loop_list, on=sel_hierarchy, how='left')

    ### CREATE MONTH COLUMN
    cost_pred['CAL_CALENDAR_MONTH'] = pd.DatetimeIndex(cost_pred[sel_datetime]).month
    cost_pred['CAL_CALENDAR_YEAR'] = pd.DatetimeIndex(cost_pred[sel_datetime]).year

    ### TRANSFORM STATUS TRUE
    transform_status = True
    st.session_state['sp_input_df_onetimecost'] = cost_onetime
    return transform_status, cost_pred, cost_onetime, loop_list


### FOOTPRINTS COST BAND PREDICTION
def input_ml_prediction():
    ### MESSAGE DATA TRANSFORMATION DONE
    time.sleep(1)
    fp_count = len(loop_list) + len(cost_onetime)
    st.success('Automated Data Transformation completed.')
    time.sleep(1)
    st.success('''
               Out of {} Dimensions, a total of {} One-Time costs were detected. \n
               The {} remaining Dimensions will be analyzed and the One-Time costs will be added later.
               '''.format(fp_count, len(cost_onetime), len(loop_list)))
    time.sleep(1)

    ### PROGRESS BAR + COLORING
    st.markdown('<style>.stProgress.st-bo{background-color: #FF4F00}</style>', unsafe_allow_html=True)
    latest_iteration = st.empty()
    bar = st.progress(0)
    start_time = datetime.datetime.now()

    ### DATAFRAMES FOR PREDICTIONS
    final_pred = pd.DataFrame([])
    norm_set = pd.DataFrame([])

    ### PREDICTIONS
    for loop_id in range(1, len(loop_list) + 1):

        ### SELECT THE RESPECTIVE LOOP ROUND
        pred_set = cost_pred[cost_pred['spance_loop_id'] == loop_id]

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
        pred_std = pd.DataFrame(pred_std).rename(columns={sel_costcol: cost_col_norm})

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
        threshold = 1.96
        cost_final = pred_set.drop([cost_col_norm], axis=1)
        pred_set = pred_set[
            (pred_set[cost_col_norm] < threshold) & (pred_set[cost_col_norm] > -threshold)].drop(
            [cost_col_norm], axis=1)

        ### TRAINING SET
        X = pred_set[['CAL_CALENDAR_MONTH', 'CAL_CALENDAR_YEAR', 'spance_row_count']]
        y = pred_set[sel_costcol]

        ### DEAL WITH SMALL TABLES: IF TOO SMALL THEN PRED = ACT /// ELSE: PREDICTION
        if len(X) == 0:
            cost_final['spance_pred_val'] = 0.0
        else:
            ### APPLY GBT AND PREDICT COSTS
            gbt = GradientBoostingRegressor(max_depth=4, alpha=0.95, max_leaf_nodes=4, n_estimators=25)
            gbt.fit(X, np.ravel(y))

        ### PREDICTION ON ACTUAL DATA
        prediction = cost_final[['CAL_CALENDAR_MONTH', 'CAL_CALENDAR_YEAR', 'spance_row_count']]
        prediction = gbt.predict(prediction)
        cost_final['spance_pred_val'] = prediction

        ### APPEND EVERYTHING TO FINAL DATASET
        final_pred = final_pred.append(cost_final)
        norm_set = norm_set.append(pred_set)

        ### DISPLAY PROGRESS BAR
        progress_time = datetime.datetime.now() - start_time
        iteration_text = 'Progress: ' + str(str(loop_id / len(loop_list) * 100)[:6]) + '% // Dimension ' + str(
            loop_id) + ' out of ' + str(len(loop_list)) + ' // Runtime: ' + str(progress_time)
        latest_iteration.text(iteration_text)
        bar.progress(loop_id / len(loop_list))

    ### RUNTIME CALCULATION
    runtime = datetime.datetime.now() - start_time
    runtime_min = runtime.seconds / 60
    runtime_sec = runtime.seconds

    if runtime_min > 1:
        runtime_min_s = round(runtime_sec - (int(runtime_min) * 60), 0)
        if runtime_min_s != 0:
            runtime_clean = str(int(round(runtime_min, 0))) + 'm ' + str(round(runtime_min_s, 0)) + 's'
        else:
            runtime_clean = str(round(runtime_min, 0)) + 'm'
    else:
        runtime_clean = str(runtime_sec) + 's'
    st.success('Data Analysis completed!')

    ### FINAL OUTPUT
    pred_status = True
    st.session_state['sp_input_status_prediction'] = True
    return pred_status, runtime_clean, final_pred, norm_set


### FOOTPRINTS CONSTRUCT FINAL DATASET
def input_ml_construct(norm_set):
    ### INTRODUCTION TEXT
    st.subheader('Predicted Hierarchy Combinations')
    st.markdown('All cost have been fully analyzed, here are some KPIs.')

    ### GENERATE STD FOR EACH LOOP + YEAR
    cost_col_std = 'spance_cost_stddev'
    norm_set = norm_set.groupby(by=['spance_loop_id', 'CAL_CALENDAR_YEAR'], as_index=False).agg(np.std).rename(
        columns={sel_costcol: cost_col_std})
    norm_set = norm_set[['spance_loop_id', 'CAL_CALENDAR_YEAR', cost_col_std]]

    ### JOIN STD WITH MAIN DATASET
    fp = pd.merge(final_pred, norm_set, on=['spance_loop_id', 'CAL_CALENDAR_YEAR'], how='left').fillna(0.0)

    ### UPPER AND LOWER BOUND
    fp['spance_pred_bound_upper'] = fp['spance_pred_val'] + fp[cost_col_std] * 1.96
    fp['spance_pred_bound_lower'] = fp['spance_pred_val'] - fp[cost_col_std] * 1.96

    ### RATING TOO LOW / TOO HIGH
    fp['spance_pred_rating'] = np.where(fp[sel_costcol] > fp['spance_pred_bound_upper'], 'Too High',
                               np.where(fp[sel_costcol] < fp['spance_pred_bound_lower'], 'Too Low','Okay'))

    ### CALCULATE ABSOLUTE DEVIATION
    fp['spance_pred_dev_abs'] = np.where(fp['spance_pred_rating'] == 'Too High', fp[sel_costcol] - fp['spance_pred_bound_upper'],
                                np.where(fp['spance_pred_rating'] == 'Too Low', fp['spance_pred_bound_lower'] - fp[sel_costcol],
                                         0.0))

    ### CALCULATE ABSOLUTE DEVIATION
    fp['spance_pred_dev_rel'] = np.where(fp['spance_pred_rating'] == 'Too High', (fp[sel_costcol] / fp['spance_pred_bound_upper'] - 1),
                                np.where(fp['spance_pred_rating'] == 'Too Low', (1 - (fp[sel_costcol] / fp['spance_pred_bound_lower'])),
                                         0.0))

    ### CLEANUP
    fp = fp.round(2)
    fp = fp.drop('index', axis=1)

    fp[sel_datetime] = fp[sel_datetime].dt.strftime('%Y-%m-%d')
    cost_onetime[sel_datetime] = cost_onetime[sel_datetime].dt.strftime('%Y-%m-%d')
    cost_data[sel_datetime] = cost_data[sel_datetime].dt.strftime('%Y-%m-%d')

    ### CALCULATE KPIs
    prediction_amount = fp.sum()[sel_costcol]
    prediction_count = len(fp)
    footprints_gen = len(loop_list) + len(cost_onetime)

    ### KPI BOXES
    kpileft, kpimidleft, kpimidright, kpiright = st.columns(4)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                runtime), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Runtime</h3>",
                    unsafe_allow_html=True)
    with kpimidleft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                num_human_format(prediction_amount)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Costs in {}</h3>".format(
            st.session_state['sp_input_selection_currency']), unsafe_allow_html=True)
    with kpimidright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{prediction_count:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Predictions</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{footprints_gen:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Dimensions</h3>", unsafe_allow_html=True)

    ### PRINT PREDICTION TABLE AND WRAP UP
    st.title(' ')
    st.markdown('This is a preview of the first 1000 columns of the final prediction.')

    fp_final = fp.drop(['spance_loop_id', 'spance_pred_val', 'spance_cost_stddev'], axis=1)
    fp_final.index += 1
    st.dataframe(fp_final.head(1000))

    st.markdown('Explore now more in the **Data Story** and the **Outlier Detection** for more insights.')
    return fp


# DISPLAY: WELCOME
input_welcome()
# DISPLAY: FILE UPLOAD
st.markdown('---')
cost_data, file_uploaded = input_upload()

# DISPLAY: SELECT HIERARCHY
if file_uploaded == True:
    st.markdown('---')
    submit_status, sel_costcol, sel_datetime, sel_hierarchy, sel_currency, hier_status = input_hierarchy(cost_data)
    pred_col = [sel_datetime] + sel_hierarchy
# DISPLAY: RUN ML TRANSFORMATION
if hier_status == True:
    st.markdown('---')
    transform_status, cost_pred, cost_onetime, loop_list = input_ml_transformation()
# ML PREDICTION
if transform_status == True:
    if st.button('Start Prediction'):
        pred_status, runtime, final_pred, norm_set = input_ml_prediction()
    else:
        pred_status = False
### RUN
if pred_status == True:
    st.write()
    st.markdown('---')
    prediction = input_ml_construct(norm_set)
    st.session_state['sp_input_df_prediction'] = prediction
    st.session_state['sp_input_df_outlier'] = prediction[prediction['spance_pred_rating'] != 'Okay']
    st.session_state['sp_input_status_prediction'] = True
# DISPLAY: FOOTER
footer()
