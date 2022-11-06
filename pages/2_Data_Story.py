# External Libraries
import altair as alt
import pandas as pd
# Internal libraries
from app_style import *


# Page Settings
page_settings('Data Story - Spance')
# Sidebar Logo
sidebar_logo('images/sp_logo.png')
# Page Header
header('Data Story')

# Data Story Welcome
def datastory_welcome():
    st.subheader('Telling your Data Story!')
    st.markdown("It's about time to dive deeper into your data. You can find 5 different sections explaining various \
                 kinds of areas of your data as a starting point for a deeper analysis.")

### FOOTPRINTS DATA STORY OVERALL KPIs
def fp_datastory_kpis():
    st.header('Overall KPIs')
    st.write('Before we start diving deeper into the data, lets get an overall look at the most important KPIs based on the predictions.')

    ### CALCULATE KPIs
    prediction_amount = prediction.sum()[predcol_cost]
    prediction_count = len(prediction)
    footprints_gen = len(prediction.groupby(by=predcol_hierarchy, axis=0, as_index=False).size())

    ### KPI BOXES
    kpileft, kpimid, kpiright = st.columns(3)
    with kpileft:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                num_human_format(prediction_amount)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Costs in {}</h3>".format(selection_currency), unsafe_allow_html=True)
    with kpimid:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{prediction_count:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Predictions</h3>", unsafe_allow_html=True)
    with kpiright:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{footprints_gen:,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>Dimensions</h3>", unsafe_allow_html=True)

### FOOTPRINTS DATA STORY COST DRIVERS
def fp_datastory_costdriver():
    # Section Header
    st.header('Main Cost Drivers')
    st.write(
        'First, we will have a look into the top cost drivers by hierarchy level. For that, please select one of your hierarchy columns to start investigate your data to find the biggest cost drivers.')

    # Hierarchy Column Selection, Top N Selection
    headleft, headright = st.columns(2)
    with headleft:
        sel_col = st.selectbox('Select a Hierarchy Column', predcol_hierarchy)
    with headright:
        topN = st.number_input('Select Top N', 2, 20, 10)

    ### TOP N TABLE
    fp_costdriver = prediction.groupby(by=sel_col, axis=0, as_index=False).sum(predcol_cost)
    fp_topn_costdriver = fp_costdriver.sort_values(by=predcol_cost, axis=0, ascending=False).head(int(topN))
    fp_topn_costdriver = fp_topn_costdriver.sort_values(by=predcol_cost, axis=0, ascending=False)

    ### HINT THAT N IS BIGGER THAN TABLE LENGTH
    if topN > len(fp_costdriver):
        st.info('The selected N is higher than the number of available values. \
                 The maximum number is {}.'.format(str(len(fp_costdriver))))

    ### COMMENTARY
    def commentary():
        ### GENERATE KPIs
        topn_amount = fp_topn_costdriver[predcol_cost].sum()
        fp_totalamt = prediction[predcol_cost].sum()

        # TEXT GENERATION 1
        text1a = 'The top '
        text1b = ' values by the overall amount in ' + selection_currency + ' for'
        text1c = ' have been selected.'

        ### TEXT1 FINAL
        text1_final = html_text(text1a) + html_highlight_kpi(int(topN)) + \
                      html_text(text1b) + html_highlight_text(sel_col) + html_text(text1c)

        # TEXT GENERATION 2
        text2a = 'Their total amount equals '
        text2b = ' which makes up more than '
        text2c = ' of the total overall cost of '
        text2d = ' in the data.'
        total_perc = str(round((topn_amount / fp_totalamt * 100), 2)) + '%'

        ### TEXT2 FINAL
        text2_final = html_text(text2a) + html_highlight_text(num_human_format(topn_amount)) + ' ' + \
                      html_highlight_text(selection_currency) + html_text(text2b) + \
                      html_highlight_text(total_perc) + html_text(text2c) + \
                      html_highlight_text(num_human_format(fp_totalamt)) + html_text(text2d)

        ### TEXT GENERATION 3
        text3a = 'The single highest cost driver is '  ### top 1 element
        text3b = ' with '  # Cost amount
        text3c = ' in total.'  ### difference to 2nd
        top1 = fp_topn_costdriver[sel_col].iloc[0]
        top1_amnt = fp_topn_costdriver[fp_topn_costdriver[sel_col] == top1][predcol_cost].iloc[0]

        ### TEXT4 FINAL
        text3_final = html_text(text3a) + html_highlight_text(top1) + html_text(text3b) + \
                      html_highlight_text(num_human_format(top1_amnt)) + html_text(text3c)

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
            text3_final = html_text(text3a) + html_highlight_text(num_human_format(diff_amnt)) + \
                          html_text(text3b) + html_highlight_kpi(unique_fp) + html_text(text3c)

            ### TEXT GENERATION 4
            text4a = 'The single highest cost driver is '  ### top 1 element
            text4b = ' with '  # Cost amount
            text4c = ' in total.'  ### difference to 2nd
            top1 = fp_topn_costdriver[sel_col].iloc[0]
            top1_amnt = fp_topn_costdriver[fp_topn_costdriver[sel_col] == top1][predcol_cost].iloc[0]

            ### TEXT4 FINAL
            text4_final = html_text(text4a) + html_highlight_text(top1) + html_text(text4b) + \
                          html_highlight_text(num_human_format(top1_amnt)) + html_text(text4c)

            return text1_final + text2_final + text3_final + text4_final

    ### CHART FOR LOWER BOUND
    chart = alt.Chart(fp_topn_costdriver).mark_bar(size=12)\
        .encode(x=alt.X(predcol_cost),
                y=alt.Y(sel_col, sort='-x'),
                color=alt.value(st.session_state['sp_color_base']),
                tooltip=[predcol_cost])\
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

    ### PREDICTION DATA
    fp_period = prediction.groupby(by=predcol_datetime, axis=0, as_index=False).sum(predcol_cost)

    ### COMMENTARY
    def commentary():
        # TEXT GENERATION 1
        text1a = 'The costs have been analyzed in a period from'
        text1b = ' to '
        text1c = ' across '
        text1d = ' different periods.'
        period_first = fp_period[predcol_datetime].min()  # First Month
        period_last = fp_period[predcol_datetime].max()  # Last Month
        period_list = fp_period[predcol_datetime].unique()  # Unique List of all the years
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
        period_avg = fp_period[predcol_cost].mean()
        value_max = fp_period[predcol_cost].max()
        value_min = fp_period[predcol_cost].min()
        per_val_max = fp_period[fp_period[predcol_cost] == value_max][predcol_datetime].iloc[0]
        per_val_min = fp_period[fp_period[predcol_cost] == value_min][predcol_datetime].iloc[0]

        # FINAL COMMENTARY
        text1_final = html_text(text1a) + html_highlight_text(period_first) + html_text(text1b) + \
                      html_highlight_text(period_last) + html_text(text1c) + html_highlight_kpi(period_count) + \
                      html_text(text1d)

        text2_final = html_text(text2a) + html_highlight_text(num_human_format(period_avg)) + ' ' +\
                      html_highlight_text(selection_currency) + html_text(text2b) + html_text(text2c) + \
                      html_highlight_text(per_val_max) + html_text(text2d) + \
                      html_highlight_text(num_human_format(value_max)) + html_text(text2e) + \
                      html_highlight_text(per_val_min) + html_text(text2f) + \
                      html_highlight_text(num_human_format(value_min)) + html_text(text2g)

        return text1_final + text2_final

    ### CHART FOR LOWER BOUND
    chart = alt.Chart(fp_period).mark_bar(size=15)\
        .encode(x=alt.X(predcol_datetime),
                y=alt.Y(predcol_cost),
                color=alt.value(st.session_state['sp_color_base']),
                tooltip=[predcol_cost])\
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

    predcol_all = predcol_hierarchy + [predcol_datetime] + [predcol_cost]

    ### ONE-TIME KPIs
    onetime_amt = onetime[predcol_cost].sum()
    onetime_gb = onetime[predcol_all].sort_values(by=predcol_cost,ascending=False).reset_index(drop=True)
    onetime_gb[predcol_cost + '_REAL'] = abs(onetime_gb[predcol_cost])

    ### ONE-TIME COSTS KPIs
    onetime_left, onetime_right = st.columns(2)
    with onetime_left:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                f'{len(onetime):,}'), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>One-Time Cost Cases</h3>", unsafe_allow_html=True)
    with onetime_right:
        st.markdown(
            "<h1 style='text-align: center; border: 2px solid #000000; border-radius: 8px; color: #FF4F00;'>{}</h1>".format(
                num_human_format(onetime_amt)), unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #000000;'>One-Time Costs in {}</h3>".format(selection_currency), unsafe_allow_html=True)

    ### ONE-TIME COSTS PER PERIOD
    st.title(' ')
    onetime_period = onetime.groupby(by=predcol_datetime,
                                     axis=0,
                                     as_index=False).size().rename(columns={'size':'Count'})

    ### PERIODICAL CHART
    def otc_chart():
        ### CHART FOR SIZE
        chart = alt.Chart(onetime_period).mark_bar(size=15) \
            .encode(x=alt.X(predcol_datetime),
                    y=alt.Y('Count'),
                    color=alt.value(color_base),
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
        periods_all = ['All'] + list(onetime[predcol_datetime].astype(str)[:7].sort_values(ascending=False).unique())
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
        otc_per = onetime[onetime[predcol_datetime].astype(str)[:7] == sel_period]
    otc_per = otc_per.sort_values(by=predcol_cost,ascending=otc_sort_ind).reset_index(drop=True).head(int(topN))
    otc_per.index += 1
    st.write(otc_per[predcol_all])

    ### OTC COMMENTARY
    def commentary():
        topOTC = otc_per[predcol_hierarchy].agg(' - '.join, axis=1).iloc[0]
        topSum = otc_per[predcol_cost].iloc[0]

        ### TEXT1
        if sel_period == 'All':
            text1a = 'The {} One-Time Cost across all periods appeared in '.format(otc_sort.lower())
            text1b = otc_per[predcol_datetime].iloc[0]
        else:
            text1a = 'The highest One-Time Cost in the selected period '
            text1b = sel_period[0]

        text1c = ' appeared for '
        text1d = ' with an total amount of '
        text1e = '{} {}'.format(num_human_format(topSum),selection_currency)

        ### TEXT1 FINAL
        text1_final = html_text(text1a) + html_highlight_text(text1b) + html_text(text1c) + \
                      html_highlight_text(topOTC) + html_text(text1d) + html_highlight_text(text1e) + '. '

        ### TEXT2
        text2a = 'Overall, the {}'.format(otc_sort.lower())
        text2b = 'Top {}'.format(int(topN))
        if not sel_period:
            text2c = ' One-Time Costs '
        else:
            text2c = ' One-Time Costs in the selected period '
        text2d = ' make up a total amount of '
        text2e = '{} {}'.format(num_human_format(otc_per[predcol_cost].sum()),selection_currency)

        ### TEXT2 FINAL
        text2_final = html_text(text2a) + html_highlight_text(text2b) + html_text(text2c) + \
                      html_text(text2d) + html_highlight_text(text2e) + '. '

        text_final = text1_final + text2_final
        st.markdown(text_final,unsafe_allow_html=True)
    commentary()

### FOOTPRINTS DATA STORY GROWERS
def fp_datastory_change():
    predcol_all = predcol_hierarchy + [predcol_datetime] + [predcol_cost]
    predcol_string = predcol_hierarchy + [predcol_datetime]

    ### SECTION HEADER
    st.header('Growers and Losers')
    st.write('The detected footprints are all unique and so is their development over the periods analyzed. \
             In this section, we are looking into the top growing and decreasing footprints in the dataset to find \
             hidden cost drivers as well as decreasing costs in certain areas.')
    st.write('Part of the analysis are only Footprints that occur in minimum 50% of the periods.')

    ### PREPARE DATA
    countPeriod = len(prediction[predcol_datetime].unique()) / 2
    prediction_okay = prediction[prediction['spance_pred_rating'] == 'Okay']

    ### FILTER FOR FOOTPRINTS WITH 50% OCCURENCE
    fp_size = prediction_okay[predcol_string].groupby(by=predcol_hierarchy, as_index=False).size()
    fp_size = fp_size[fp_size['size'] >= countPeriod]
    fp_period = pd.merge(prediction_okay, fp_size, on=predcol_hierarchy)

    ### FILTER FOR FOOTPRINTS IN MIN AND MAX PERIOD
    fp_max = fp_period[predcol_string].groupby(by=predcol_hierarchy,as_index=False).max()
    fp_min = fp_period[predcol_string].groupby(by=predcol_hierarchy, as_index=False).min()

    fp_clean = prediction_okay[predcol_all]
    fp_max = pd.merge(fp_clean, fp_max, on=list(fp_max.columns)).rename(columns={predcol_datetime : 'AMOUNT_LAST'})
    fp_min = pd.merge(fp_clean, fp_min, on=list(fp_min.columns)).rename(columns={predcol_datetime : 'AMOUNT_FIRST'})

    ### CALCULATE DIFFERENCE
    fp_change = pd.merge(fp_max,fp_min,on=predcol_hierarchy)
    fp_change = fp_change[fp_change['AMOUNT_FIRST'] != 0]
    fp_change['CHANGE_ABS'] = fp_change['AMOUNT_LAST'] - fp_change['AMOUNT_FIRST']
    fp_change['CHANGE_REL'] = round((fp_change['CHANGE_ABS'] / fp_change['AMOUNT_FIRST']) * 100, 0)
    fp_change = pd.merge(fp_change,fp_size,on=predcol_hierarchy).rename(columns={'size':'PERIODS'})

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
        text1_final = html_text(text1a) + html_highlight_text(text1b) + html_text(text1c) + \
                      html_text(text1d) + html_highlight_text(text1e) + '.'

        ### TEXT 2 COMMENTARY
        text2a = 'The top Footprint by'
        if abs_rel == 'Absolute':
            text2b = 'absolute change is '
        else:
            text2b = 'relative change is '
        text2c = fp_change[predcol_hierarchy].agg(' - '.join, axis=1).iloc[0]
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
        text2_final = html_text(text2a) + html_text(text2b) + html_highlight_text(text2c) + \
                      html_text(text2d) + html_highlight_text(text2e) + html_text(text2f) + \
                      html_highlight_text(text2g) + '.'

        ### FINAL TEXT
        final_text = text1_final + text2_final


        return st.markdown(final_text,unsafe_allow_html=True)
    comment_table()
    ### SPACING
    st.subheader('  ')

    ### DISPLAY FOOTPRINTS
    fp_change['RANK'] = fp_change.index
    fp_change['RANK'] = fp_change['RANK'].astype(str)
    fp_col = ['RANK'] + predcol_hierarchy
    fp_change['FP_KEY1'] = fp_change[predcol_hierarchy].agg(' - '.join, axis=1)
    fp_change['FP_KEY2'] = fp_change[fp_col].agg(' - '.join, axis=1)

    ### HEADER AND TEXT
    st.subheader('Footprint Deep Dive')
    st.write('Select the selected top footprints from above to analyze their trends.')

    ### FILTER PREDICTION TABLE
    fp_select = st.selectbox('Footprint Selection',fp_change['FP_KEY2'])
    fp_key = fp_change[fp_change['FP_KEY2'] == fp_select]['FP_KEY1'].iloc[0]
    prediction_okay['FP_KEY1'] = prediction_okay[predcol_hierarchy].agg(' - '.join, axis=1)
    fp = prediction_okay[prediction_okay['FP_KEY1'] == fp_key]

    ### DISPLAY CHART
    def fp_chart():
        ### CHART FOR LOWER BOUND
        chart_low = alt.Chart(fp).mark_line(strokeDash=[1,1], point=True)\
            .encode(x=alt.X(predcol_datetime),
                    y=alt.Y('FP_LOWER_BOUND'),
                    color=alt.value(color_base),
                    tooltip=[predcol_datetime,'FP_LOWER_BOUND',predcol_cost,'FP_UPPER_BOUND']) \
            .interactive()

        ### CHART FOR ACTUAL COSTS
        chart_act = alt.Chart(fp).mark_line(point=True)\
            .encode(x=alt.X(predcol_datetime),
                    y=alt.Y(predcol_cost),
                    color=alt.value(color_base),
                    tooltip=[predcol_datetime,'FP_LOWER_BOUND',predcol_cost,'FP_UPPER_BOUND'])\
            .interactive()

        ### CHART FOR UPPER BOUND
        chart_up = alt.Chart(fp).mark_line(strokeDash=[1,1], point=True)\
            .encode(x=alt.X(predcol_datetime),
                    y=alt.Y('FP_UPPER_BOUND'),
                    color=alt.value(color_base),
                    tooltip=[predcol_datetime,'FP_LOWER_BOUND',predcol_cost,'FP_UPPER_BOUND'])\
            .interactive()

        ### MERGE ALL CHARTS
        chart = alt.layer(chart_low, chart_act, chart_up)
        return st.altair_chart(chart, use_container_width=True)
    ### HEADER
    fp_chart()


# DISPLAY: RUN THE PAGE
# Call session states
prediction, raw_data, onetime, predcol_cost, \
predcol_hierarchy, predcol_datetime, selection_currency, \
color_base = call_session_state()

# Run page functions
try:
    ### FP WELCOME
    datastory_welcome()
    ### FP PREDICTION CHECK
    app_predcheck()
    ### SPACING
    st.markdown('---')
    ### FP OVERALL RESULT
    fp_datastory_kpis()
    ### SPACING
    st.markdown('---')
    ### FP COST DRIVERS
    fp_datastory_costdriver()
    # ### SPACING
    st.markdown('---')
    # ### FP PERIODICAL ANALYSIS
    fp_datastory_periods()
    ### SPACING
    st.markdown('---')
    ### FP ONE-TIME COSTS
    fp_datastory_onetime()
    ### SPACING
    # st.markdown('---')
    # ### FP CHANGES
    # fp_datastory_change()
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
