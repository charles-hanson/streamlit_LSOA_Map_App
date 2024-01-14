import streamlit as st
import pandas as pd
from datetime import date

# Initialize session state
if 'map_df' not in st.session_state:
    st.session_state.map_df = None

if 'omni_df' not in st.session_state:
    st.session_state.omni_df = None

if 'completion_df' not in st.session_state:
    st.session_state.completion_df = None

if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None

boy_df = pd.read_csv('MapReport/boy.csv', dtype=str)
tab1, tab2, tab3, tab4 = st.tabs(["MAP Upload", "Omni Report Upload", "Report Output", "Data Summary"])

st.sidebar.header("LSOA Map Rollup Report Creator")

# Upload MAP Report
try:
    map_file = st.sidebar.file_uploader("Map Report file as Excel (.xlsx)")

    if map_file:
        st.session_state.map_df = pd.read_excel(map_file)
        st.session_state.map_df = st.session_state.map_df[["Student ID", "Subject"]]
        st.session_state.map_df['Student ID'] = st.session_state.map_df['Student ID'].astype(str)
        student_df = st.session_state.map_df.copy()
        student_df = student_df[["Student ID"]]
        student_df.drop_duplicates(subset=['Student ID'], inplace=True)
        rla_df = st.session_state.map_df.copy()
        rla_df = rla_df[rla_df["Subject"] == "Language Arts"]
        rla_df.rename(columns={'Subject': 'MOY MAP RLA'}, inplace=True)
        mth_df = st.session_state.map_df.copy()
        mth_df = mth_df[mth_df["Subject"] == "Mathematics"]
        mth_df.rename(columns={'Subject': 'MOY MAP MATH'}, inplace=True)
        completion_df = student_df.merge(rla_df, how="left", on="Student ID")
        completion_df = completion_df.merge(mth_df, how="left", on="Student ID")
        completion_df['MOY MAP Completed'] = ""
        completion_df.loc[completion_df['MOY MAP RLA'] == 'Language Arts', 'MOY MAP RLA'] = "Yes"
        completion_df.loc[completion_df['MOY MAP RLA'] != 'Yes', 'MOY MAP RLA'] = "No"
        completion_df.loc[completion_df['MOY MAP MATH'] == 'Mathematics', 'MOY MAP MATH'] = "Yes"
        completion_df.loc[completion_df['MOY MAP MATH'] != 'Yes', 'MOY MAP MATH'] = "No"
        completion_df.loc[
            (completion_df['MOY MAP RLA'] == "Yes") & (completion_df['MOY MAP MATH'] == "Yes"), 'MOY MAP Completed'] = "Yes"
        completion_df.loc[completion_df['MOY MAP MATH'] != 'Yes', 'MOY MAP Completed'] = "No"
        tab1.dataframe(completion_df)
        st.sidebar.success("MAP file successfully uploaded.")
except:
    st.sidebar.warning("Please upload your MAP file.")

# Upload Omni Report
try:
    omni_file = st.sidebar.file_uploader("Omni file as CSV (.csv)")

    if omni_file:
        st.session_state.omni_df = pd.read_csv(omni_file, dtype=str)
        omni_df = st.session_state.omni_df.loc[st.session_state.omni_df['SCHOOL'] == (
            "Lone Star Online Academy @ Roscoe")]
        omni_df['SCHOOLENROLLDATE'] = pd.to_datetime(omni_df['SCHOOLENROLLDATE']).dt.date
        today = date.today()
        omni_df = omni_df[omni_df['SCHOOLENROLLDATE'] <= today]
        omni_df = omni_df[["STUDENTID", "IDENTITYID", "SCHOOLENROLLDATE"]]
        tab2.dataframe(omni_df)
        st.sidebar.success("Omni file successfully uploaded.")
except:
    st.sidebar.warning("Please upload your Omni file.")

# Merge and Data Summary
try:
    if tab3.button("Merge"):
        merged_df = omni_df.merge(boy_df, how="left", left_on="STUDENTID", right_on="Student ID",
                                                   indicator="_boy")
        merged_df = merged_df.merge(st.session_state.completion_df, how="left", left_on="IDENTITYID",
                                    right_on="Student ID", indicator="_merged")
        merged_df = merged_df[["STUDENTID", "BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed", "MOY MAP RLA",
                               "MOY MAP MATH", "MOY MAP Completed"]]
        merged_df.loc[(merged_df['BOY MAP Completed'] != "Yes") & (
                    merged_df['BOY MAP Completed'] != "No"), ["BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed"]] = "N/A"
        merged_df.loc[merged_df['MOY MAP RLA'] == 'Language Arts', 'MOY MAP RLA'] = "Yes"
        merged_df.loc[merged_df['MOY MAP RLA'] != 'Yes', 'MOY MAP RLA'] = "No"
        merged_df.loc[merged_df['MOY MAP MATH'] == 'Mathematics', 'MOY MAP MATH'] = "Yes"
        merged_df.loc[merged_df['MOY MAP MATH'] != 'Yes', 'MOY MAP MATH'] = "No"
        merged_df.loc[
            (merged_df['MOY MAP RLA'] == "Yes") & (st.session_state.completion_df['MOY MAP MATH'] == "Yes"),
            'MOY MAP Completed'] = "Yes"
        merged_df.loc[merged_df['MOY MAP Completed'] != 'Yes', 'MOY MAP Completed'] = "No"

        st.session_state.merged_df = merged_df
        tab3.dataframe(merged_df)
        tab3.write(merged_df.describe())
except:
    st.warning("Please upload both files above")

# Data Summary
map_session = tab4.selectbox("Pick one", ["BOY", "MOY"])
try:
    if map_session == "BOY":
        st.dataframe(st.session_state.merged_df[['STUDENTID', 'BOY MAP RLA', 'BOY MAP MATH', 'BOY MAP Completed']])
    elif map_session == "MOY":
        st.dataframe(st.session_state.merged_df[['STUDENTID', 'MOY MAP RLA', 'MOY MAP MATH', 'MOY MAP Completed']])
except:
    pass
