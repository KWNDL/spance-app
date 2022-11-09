# External Libraries
import altair as alt
import pandas as pd
import streamlit as st
import math
import datetime
# Internal libraries
from app_style import *


# Page Settings
page_settings('Forecasting - Spance')
# Sidebar Logo
sidebar_logo('images/sp_logo_header.png')
# Page Header
header('Forecasting')

# prediction, raw_data, onetime, outlier, predcol_cost, \
# predcol_hierarchy, predcol_datetime, predcol_datetime_dt, selection_currency, \
# color_base = call_session_state()
#
# # Calculate Number of Maximum Periods for Forecast
# fcMaxPeriods = math.ceil(len(prediction.groupby(predcol_datetime_dt)) * 0.5)
# maxPeriod = str(prediction[predcol_datetime].agg(['max'])[0])
#
# # Forecast Period Slider and Selection
# fcPeriods = st.slider('Forecast Periods',1,fcMaxPeriods,math.ceil(fcMaxPeriods / 2))
#
# # Time Granularity Algorithm
# def get_granularity():
#     gran_df = pd.DataFrame(prediction[predcol_datetime])
#     gran_df['day'] = pd.DatetimeIndex(gran_df[predcol_datetime]).day
#     dayCheck = gran_df['day'].nunique()
#
#     if dayCheck == 1:
#         granularity = 'M'
#     else:
#         granularity = 'D'
#     return granularity
#
# timeGranularity = get_granularity()
#
# # Create Forecast Base Table
# fcBaseTable = pd.DataFrame(pd.date_range(start = maxPeriod, periods = fcPeriods + 1, freq=timeGranularity).to_pydatetime())
# fcBaseTable = pd.DataFrame(fcBaseTable.iloc[1:].to_numpy().astype('datetime64[M]'),columns=[predcol_datetime])
# fcBaseTable['CAL_CALENDAR_MONTH'] = pd.DatetimeIndex(fcBaseTable[predcol_datetime]).month
# fcBaseTable['CAL_CALENDAR_YEAR'] = pd.DatetimeIndex(fcBaseTable[predcol_datetime]).year
#
# st.dataframe(fcBaseTable)
# st.dataframe(prediction)











# Page Under Construction
st.info('Page under construction. Please come back later!')
# Footer
footer()
