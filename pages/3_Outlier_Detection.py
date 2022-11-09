# External Libraries
import streamlit as st
import altair as alt
import pandas as pd
# Internal libraries
from app_style import *


# Page Settings
page_settings('Outlier Detection - Spance')
# Sidebar Logo
sidebar_logo('images/sp_logo_header.png')
# Page Header
header('Outlier Detection')

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
    outlier_high = len(outlier[outlier['spance_pred_rating'] == 'Too High'])
    outlier_low = len(outlier[outlier['spance_pred_rating'] == 'Too Low'])
    deviation_sum = outlier['spance_pred_dev_abs'].sum()

    # KPI Boxes in 4 columns
    kpileft, kpimidleft, kpimidright, kpiright = st.columns(4)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{len(prediction):,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Predictions</h3>".format(selection_currency),unsafe_allow_html=True)
    with kpimidleft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{outlier_high:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Too High</h3>", unsafe_allow_html=True)
    with kpimidright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{outlier_low:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Too Low</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                num_human_format(deviation_sum)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Deviation in {}</h3>".format(selection_currency), unsafe_allow_html=True)

### FOOTPRINTS OUTLIER PER PERIOD
def fp_outliers_periods():
    st.header('Outliers by Period')
    st.write('View when how many outliers appeared in each analyzed period by the outlier count and expected deviation amount.')

    # Count per Outlier Rating per Period
    outlier_cnt = outlier.groupby(
        by=[predcol_datetime,'spance_pred_rating'], axis=0, as_index=False).size()
    outlier_amt = outlier.groupby(
        by=[predcol_datetime,'spance_pred_rating'], axis=0, as_index=False).sum('spance_pred_dev_abs')[[predcol_datetime,'spance_pred_rating','spance_pred_dev_abs']]

    ### TAB WITH CHARTS
    tab1, tab2 = st.tabs(["Amount", "Occurence"])

    with tab1:
        chart = alt.Chart(outlier_amt).mark_bar().encode(
                    x=alt.X('spance_pred_rating:O', title=None),
                    y=alt.Y('spance_pred_dev_abs:Q', title=None),
                    column=alt.Column(predcol_datetime, title=None),
                    color=alt.Color('spance_pred_rating',scale=alt.Scale(range=['#FF4F00', '#DCDCDC']),legend=None),
                    tooltip=[predcol_datetime,'spance_pred_dev_abs']) \
                .configure_view(strokeWidth=0.0) \
                .interactive()
        st.altair_chart(chart)

    with tab2:
        ### CHART FOR SIZE
        chart = alt.Chart(outlier_cnt).mark_bar().encode(
                    x=alt.X('spance_pred_rating:O', title=None),
                    y=alt.Y('size:Q', title=None),
                    column=alt.Column(predcol_datetime, title=None),
                    color=alt.Color('spance_pred_rating', scale=alt.Scale(range=['#FF4F00','#DCDCDC']),legend=None),
                    tooltip=[predcol_datetime,'size']) \
            .configure_view(strokeWidth=0.0) \
            .interactive()
        st.altair_chart(chart)

### FOOTPRINTS OUTLIER PER HIERARCHY
def fp_outliers_hierarchy():

    st.header('Outliers by Hierarchy')
    st.write('Find the origin of outliers by your hierarchy based on Deviation Amount or Outlier Count.')

    ### SELECTION BOXES
    left, right = st.columns(2)
    with left:
        view_select_dimension = st.multiselect('Select Hierarchy Columns', predcol_hierarchy)
    with right:
        sel_type = st.selectbox('Sort Outliers by',['Amount','Occurence'])

    ### GET TOP N SLIDER
    topN = st.slider('Select Top N Outliers', 1, 25, 10,help='Maximum Top N is 25.')

    ### GENERATE THE TABLE
    if not view_select_dimension:
        st.info('Please select a hierarchy column.')
    else:
        ### CALCULATE DEVIATION AMOUNT
        outl_amt = outlier.groupby(view_select_dimension,as_index=False).sum()[view_select_dimension + [predcol_cost]]
        outl_amt = outl_amt.rename(columns={predcol_cost : 'Amount'}).reset_index(drop=True)

        ### CALCULATE OUTLIER COUNT
        outl_cnt = outlier.groupby(view_select_dimension, as_index=False).size()[view_select_dimension + ['size']]
        outl_cnt = outl_cnt.rename(columns={'size': 'Occurence'}).reset_index(drop=True)

        ### FINALIZE TABLE
        hier_table = pd.merge(outl_amt,outl_cnt,how='outer',on=view_select_dimension)
        if sel_type == 'Amount':
            hier_table = hier_table.sort_values(by='Amount',axis=0,ascending=False)[:topN]
            hier_table['Amount'] = hier_table.apply(lambda row: num_human_format(row['Amount']), axis=1)
            hier_table = hier_table.reset_index(drop=True)
            hier_table.index += 1
        else:
            hier_table = hier_table.sort_values(by='Occurence', axis=0, ascending=False)[:topN]
            hier_table['Amount'] = hier_table.apply(lambda row: num_human_format(row['Amount']), axis=1)
            hier_table = hier_table.reset_index(drop=True)
            hier_table.index += 1

        if len(hier_table) < topN:
            st.info('Selection has less elements than Top N selection (Max = ' + str(len(outl_cnt)) + ').')

        st.write(hier_table)

### FOOTPRINTS TOP OUTLIERS
def fp_outliers_top_outliers():
    st.header('Top Single Outliers by Hierarchy')
    st.write('Check the top outliers in the selected period.')

    periods_all = prediction[predcol_datetime].unique()
    outl_left, outl_right = st.columns(2)
    with outl_left:
        sel_period = st.selectbox('Periodical Selection',periods_all,help='Select Period you would like to analyze closer.')
        st.session_state['spance_outliers_period'] = sel_period
    with outl_right:
        sel_devtype = st.selectbox('Deviation Type',['All','Too Low','Too High'],help='Selection between All, Too High or Too Low deviations.')


    ### SLIDER FOR TOP N VALUES
    topN = st.slider('Select Top Single Outliers',1,25,value=10,help='Maximum Top N is 25.')

    ### FILTER DEVIATION TYPES
    if sel_devtype != 'All':
        outlier_table = outlier[outlier['spance_pred_rating'] == sel_devtype]
    else:
        outlier_table = outlier

    ### FILTER TABLE AND SORT BY ABSOLUTE DEVIATION
    outlier_table = outlier_table[outlier_table[predcol_datetime] == sel_period]
    outlier_table = outlier_table.sort_values(by='spance_pred_dev_abs', ascending=False).reset_index(drop=True)

    ### SELECT COLUMNS AND FILTER FOR TOPN
    outlier_table['RANK'] = outlier_table.index + 1
    outlier_cols = ['RANK'] + predcol_hierarchy + [predcol_datetime,'spance_pred_rating','spance_pred_bound_upper',predcol_cost,'spance_pred_bound_lower','spance_pred_dev_abs']
    outlier_table = outlier_table[outlier_cols][:topN]
    outlier_table.index += 1

    ### REFORMATTING NUMERICAL COLUMNS
    for col in ['spance_pred_bound_lower',predcol_cost,'spance_pred_bound_upper','spance_pred_dev_abs']:
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

    sel_period = st.session_state['spance_outliers_period']

    ### CALCULATE KEY COLUMNS TO CROSS-FILTER
    filter_col = ['RANK'] + predcol_hierarchy
    outlier_table['RANK'] = outlier_table['RANK'].astype(str)
    outlier_table['FP_KEY1'] = outlier_table[filter_col].agg(' - '.join, axis=1)
    outlier_table['FP_KEY2'] = outlier_table[predcol_hierarchy].agg(' - '.join, axis=1)

    ### FOOTPRINTS SELECTION
    sel_fp = st.selectbox('Select Footprint',outlier_table['FP_KEY1'])
    outlier_tab = outlier_table[outlier_table['FP_KEY1'] == sel_fp]

    ### FILTER TRANSACTIONAL TABLE
    footprint_name = outlier_tab['FP_KEY2'].iloc[0]
    prediction['FP_KEY1'] = prediction[predcol_hierarchy].agg(' - '.join, axis=1)
    raw_filter = prediction[prediction['FP_KEY1'] == footprint_name]

    ### CREATE CHART DATA
    st.subheader('Footprint Development')
    st.subheader(' ')
    filter_col = predcol_hierarchy + [predcol_datetime,'spance_pred_bound_lower',predcol_cost,'spance_pred_bound_upper','spance_pred_rating','spance_pred_dev_abs']
    footprint = raw_filter[filter_col]

    ### CHART FOR LOWER BOUND
    chart_low = alt.Chart(footprint).mark_line(strokeDash=[1,1], point=True)\
        .encode(x=alt.X(predcol_datetime),
                y=alt.Y('spance_pred_bound_lower'),
                color=alt.value('#FF4F00'),
                tooltip=[predcol_datetime,'spance_pred_rating','spance_pred_bound_lower',predcol_cost,'spance_pred_bound_upper','spance_pred_dev_abs'])\
        .interactive()

    ### CHART FOR ACTUAL COSTS
    chart_act = alt.Chart(footprint).mark_line(point=True)\
        .encode(x=alt.X(predcol_datetime,title=None),
                y=alt.Y(predcol_cost,title=None),
                color=alt.value('#000000'),
                tooltip=[predcol_datetime,'spance_pred_rating','spance_pred_bound_lower',predcol_cost,'spance_pred_bound_upper','spance_pred_dev_abs'])\
        .interactive()

    ### CHART FOR UPPER BOUND
    chart_up = alt.Chart(footprint).mark_line(strokeDash=[1,1], point=True)\
        .encode(x=alt.X(predcol_datetime,title=None),
                y=alt.Y('spance_pred_bound_upper',title=None),
                color=alt.value('#FF4F00'),
                tooltip=[predcol_datetime,'spance_pred_rating','spance_pred_bound_lower',predcol_cost,'spance_pred_bound_upper','spance_pred_dev_abs'])\
        .interactive()

    ### MERGE ALL CHARTS
    chart = alt.layer(chart_low, chart_act, chart_up)
    st.altair_chart(chart, use_container_width=True)

    ### FOOTPRINT COMMENTARY
    def commentary():

        ### COMMENTARY KPIs
        period_count = len(footprint)
        fp_name = footprint_name
        outlier_count = len(footprint[footprint['spance_pred_rating'] != 'Okay'])
        curr_per_outl = footprint[footprint[predcol_datetime] == sel_period]['spance_pred_rating'].iloc[0]
        curr_costs = footprint[footprint[predcol_datetime] == sel_period][predcol_cost].iloc[0]
        curr_dev = footprint[footprint[predcol_datetime] == sel_period]['spance_pred_dev_abs'].iloc[0]
        outl_quota = str(round((outlier_count / period_count) * 100,2)) + '%'

        ### TEXT1
        text1a = 'The selected footprint '
        text1b = ' shows for the selected period of '
        text1c = ' an outlier with a '
        text1d = ' indicator.'

        text1 = html_text(text1a) + html_highlight_text(fp_name) + html_text(text1b) + html_highlight_text(sel_period) + \
                html_text(text1c) + html_highlight_text(curr_per_outl) + html_text(text1d)

        ### TEXT2
        text2a = ' The actual amount of '
        text2b = ' deviates '
        text2c = ' from the initially expected amount.'

        text2 = html_text(text2a) + html_highlight_text(num_human_format(curr_costs)) + ' ' + html_highlight_text(selection_currency) + \
                html_text(text2b) + html_highlight_text(num_human_format(curr_dev)) + ' ' + html_highlight_text(selection_currency) + html_text(text2c)

        ### TEXT3
        text3a = 'Along the '
        text3b = ' different periods, the footprint showed '
        text3c = ' outliers which equals to an outlier quota of '
        text3d = '.'

        text3 = html_text(text3a) + html_highlight_kpi(period_count) + html_text(text3b) + \
                html_highlight_kpi(outlier_count) + html_text(text3c) + html_highlight_text(outl_quota) + \
                html_text(text3d)

        ### DISPLAY FINAL TEXT
        final_text = text1 + text2 + text3
        return st.markdown(final_text,unsafe_allow_html=True)
    commentary()

    ### TRANSACTIONAL BREAKDOWN
    st.subheader('  ')
    st.subheader('Raw Data Breakdown')
    st.markdown('In this section is a further breakdown of the data of the \
                 selected footprint based on the original input data.')

    ### FILTER RAW DATA
    raw_data = st.session_state['sp_input_df_rawdata']
    raw_data['FP_NAME'] = raw_data[predcol_hierarchy].agg(' - '.join, axis=1)
    raw_data = raw_data[(raw_data['FP_NAME'] == footprint_name) & (raw_data[predcol_datetime] == sel_period)]
    raw_data = raw_data.sort_values(by=predcol_cost,ascending=False).drop('FP_NAME',axis=1).reset_index(drop=True)

    ### FINALIZE RAW DATA TABLE
    raw_data.index += 1
    st.dataframe(raw_data)


# DISPLAY: RUN THE PAGE
# Call session states


# Run App
try:
    # Call session states into the script
    prediction, raw_data, onetime, outlier, predcol_cost, \
    predcol_hierarchy, predcol_datetime, selection_currency, \
    color_base = call_session_state()
    ### FP WELCOME
    fp_outliers_welcome()
    ### FP PREDICTION CHECK
    app_predcheck()
    ### SPACING
    st.markdown('---')
    ### FP OVERALL RESULT
    fp_outliers_kpis()
    ### SPACING
    st.markdown('---')
    ### FP COST DRIVERS
    fp_outliers_periods()
    # ### SPACING
    st.markdown('---')
    # ### FP PERIODICAL ANALYSIS
    fp_outliers_hierarchy()
    ### SPACING
    st.markdown('---')
    ### FP ONE-TIME COSTS
    outlier_table, check_indicator = fp_outliers_top_outliers()
    ### SPACING
    st.markdown('---')
    ### FP CHANGES
    fp_outliers_footprints()
    # DISPLAY: FOOTER
    footer()
except KeyError:
    # DISPLAY: ERROR, RUN PREDICTION FIRST
    st.info('''
            No prediction available yet. \n
            Run a prediction in the Data Input page and come back again.
            ''')
    # DISPLAY: FOOTER
    footer()
