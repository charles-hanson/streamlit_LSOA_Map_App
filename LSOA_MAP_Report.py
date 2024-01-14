import streamlit as st
import pandas as pd
from datetime import date

# Function to read and process MAP file
@st.cache_data
def process_map_file(map_file):
    map_df = pd.read_excel(map_file)
    map_df = map_df[["Student ID", "Subject"]]
    map_df['Student ID'] = map_df['Student ID'].astype(str)
    student_df = map_df.copy()
    student_df = student_df[["Student ID"]]
    student_df.drop_duplicates(subset=['Student ID'], inplace=True)
    rla_df = map_df.copy()
    rla_df = rla_df[rla_df["Subject"] == "Language Arts"]
    rla_df.rename(columns={'Subject': 'MOY MAP RLA'}, inplace=True)
    mth_df = map_df.copy()
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
    return completion_df

# Function to read and process Omni file
@st.cache_data
def process_omni_file(omni_file):
    omni_df = pd.read_csv(omni_file, dtype=str)
    omni_df = omni_df.loc[omni_df['SCHOOL'] == ("Lone Star Online Academy @ Roscoe")]
    omni_df['SCHOOLENROLLDATE'] = pd.to_datetime(omni_df['SCHOOLENROLLDATE']).dt.date
    today = date.today()
    omni_df = omni_df[omni_df['SCHOOLENROLLDATE'] <= today]
    omni_df = omni_df[["STUDENTID", "IDENTITYID", "SCHOOLENROLLDATE"]]
    return omni_df

boy_df = pd.read_csv("boy_json.json")
tab1, tab2, tab3, tab4 = st.tabs(["MAP Upload", "Omni Report Upload", "Report Output", "Data Summary"])

st.sidebar.header("LSOA Map Rollup Report Creator")

# Upload MAP Report
map_file = st.sidebar.file_uploader("Map Report file as Excel (.xlsx)", type=["xlsx"])
if map_file:
    completion_df = process_map_file(map_file)
    tab1.dataframe(completion_df)
    st.sidebar.success("MAP file successfully uploaded.")

# Upload Omni Report
omni_file = st.sidebar.file_uploader("Omni file as CSV (.csv)", type=["csv"])
if omni_file:
    omni_df = process_omni_file(omni_file)
    tab2.dataframe(omni_df)
    st.sidebar.success("Omni file successfully uploaded.")

# Merge and Data Summary
try:
    if tab3.button("Merge"):
        merged_df = omni_df.merge(boy_df, how="left", left_on="STUDENTID", right_on="Student ID", indicator="_boy")
        merged_df = merged_df.merge(completion_df, how="left", left_on="IDENTITYID", right_on="Student ID",
                                    indicator="_merged")
        merged_df = merged_df[["STUDENTID", "BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed", "MOY MAP RLA",
                               "MOY MAP MATH", "MOY MAP Completed"]]
        merged_df.loc[(merged_df['BOY MAP Completed'] != "Yes") & (
                merged_df['BOY MAP Completed'] != "No"), ["BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed"]] = "N/A"
        merged_df.loc[merged_df['MOY MAP RLA'] == 'Language Arts', 'MOY MAP RLA'] = "Yes"
        merged_df.loc[merged_df['MOY MAP RLA'] != 'Yes', 'MOY MAP RLA'] = "No"
        merged_df.loc[merged_df['MOY MAP MATH'] == 'Mathematics', 'MOY MAP MATH'] = "Yes"
        merged_df.loc[merged_df['MOY MAP MATH'] != 'Yes', 'MOY MAP MATH'] = "No"
        merged_df.loc[
            (merged_df['MOY MAP RLA'] == "Yes") & (completion_df['MOY MAP MATH'] == "Yes"), 'MOY MAP Completed'] = "Yes"
        merged_df.loc[merged_df['MOY MAP Completed'] != 'Yes', 'MOY MAP Completed'] = "No"

        tab3.dataframe(merged_df)
        
        boy_yes= merged_df['BOY MAP Completed'].eq('Yes').sum()
        boy_no= merged_df['BOY MAP Completed'].eq('No').sum()
        boy_na=merged_df['BOY MAP Completed'].eq('N/A').sum()
        boy_total=len(merged_df["BOY MAP Completed"])
        boy_percent_yes=round(boy_yes/boy_total *100)
        boy_percent_no=round(boy_no/boy_total *100)
        boy_percent_na=round(boy_na/boy_total *100)
        boy_percent_total=boy_percent_yes+boy_percent_no+boy_percent_na
        
        moy_yes= merged_df['MOY MAP Completed'].eq('Yes').sum()
        moy_no= merged_df['MOY MAP Completed'].eq('No').sum()
        moy_na=merged_df['MOY MAP Completed'].eq('N/A').sum()
        moy_total=len(merged_df["MOY MAP Completed"
        ])
        moy_percent_yes=round(moy_yes/moy_total *100)
        moy_percent_no=round(moy_no/moy_total *100)
        moy_percent_na=round(moy_na/moy_total *100)
        moy_percent_total=moy_percent_yes+moy_percent_no+moy_percent_na
        
        
        metrics_df = pd.DataFrame({'Metric': ['Yes', 'No', 'N/A', 'Total'],
        'BOY Map#': [boy_yes,boy_no,boy_na,boy_total],
        'BOY Map %': [boy_percent_yes, boy_percent_no, boy_percent_na, boy_percent_total],
        'MOY Map #': [moy_yes, moy_no, moy_na, moy_total],
        'MOY Map %': [moy_percent_yes, moy_percent_no, moy_percent_na, moy_percent_total],
        })
        tab4.dataframe(metrics_df)

except Exception as e:
    st.warning(f"Please upload both files above. Error: {e}")

# Data Summary

# try:
    

# except Exception as e:
#     st.warning(f"Error: {e}")


