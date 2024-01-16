import streamlit as st
import pandas as pd
from datetime import date

#Function to read and process BOY MAP file
@st.cache_data()
def process_boy_map_file(map_file):
    if map_file.name.endswith('.csv'):
        map_df = pd.read_csv(map_file, dtype=str)
    elif map_file.name.endswith('.xlsx'):
        map_df = pd.read_excel(map_file, engine='openpyxl')
    else:
        # Handle unsupported file types
        st.sidebar.error("Unsupported file format for BOY Map Report. Please upload either CSV or XLSX.")
        return None
    map_df = map_df[["Student ID", "Subject"]]
    map_df['Student ID'] = map_df['Student ID'].astype(str)
    student_df = map_df.copy()
    student_df = student_df[["Student ID"]]
    student_df.drop_duplicates(subset=['Student ID'], inplace=True)
    rla_df = map_df.copy()
    rla_df = rla_df[rla_df["Subject"] == "Language Arts"]
    rla_df.rename(columns={'Subject': 'BOY MAP RLA'}, inplace=True)
    mth_df = map_df.copy()
    mth_df = mth_df[mth_df["Subject"] == "Mathematics"]
    mth_df.rename(columns={'Subject': 'BOY MAP MATH'}, inplace=True)
    completion_df = student_df.merge(rla_df, how="left", on="Student ID")
    completion_df = completion_df.merge(mth_df, how="left", on="Student ID")
    completion_df['BOY MAP Completed'] = ""
    completion_df.loc[completion_df['BOY MAP RLA'] == 'Language Arts', 'BOY MAP RLA'] = "Yes"
    completion_df.loc[completion_df['BOY MAP RLA'] != 'Yes', 'BOY MAP RLA'] = "No"
    completion_df.loc[completion_df['BOY MAP MATH'] == 'Mathematics', 'BOY MAP MATH'] = "Yes"
    completion_df.loc[completion_df['BOY MAP MATH'] != 'Yes', 'BOY MAP MATH'] = "No"
    completion_df.loc[
        (completion_df['BOY MAP RLA'] == "Yes") & (completion_df['BOY MAP MATH'] == "Yes"), 'BOY MAP Completed'] = "Yes"
    completion_df.loc[completion_df['BOY MAP MATH'] != 'Yes', 'BOY MAP Completed'] = "No"
    return completion_df

# Function to read and process MOY MAP file
@st.cache_data()
def process_moy_map_file(map_file):
    if map_file.name.endswith('.csv'):
        map_df = pd.read_csv(map_file, dtype=str)
    elif map_file.name.endswith('.xlsx'):
        map_df = pd.read_excel(map_file, engine='openpyxl')
    else:
        # Handle unsupported file types
        st.sidebar.error("Unsupported file format for BOY Map Report. Please upload either CSV or XLSX.")
        return None
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
@st.cache_data()
def process_omni_file(omni_file):
    if omni_file.name.endswith('.csv'):
        omni_df = pd.read_csv(omni_file, dtype=str)
    elif map_file.name.endswith('.xlsx'):
        omni_df = pd.read_excel(omni_file, engine='openpyxl')
    else:
        # Handle unsupported file types
        st.sidebar.error("Unsupported file format for BOY Map Report. Please upload either CSV or XLSX.")
        return None
  
    omni_df = omni_df.loc[omni_df['SCHOOL'] == ("Lone Star Online Academy @ Roscoe")]
    omni_df['SCHOOLENROLLDATE'] = pd.to_datetime(omni_df['SCHOOLENROLLDATE']).dt.date
    today = date.today()
    omni_df = omni_df[omni_df['SCHOOLENROLLDATE'] <= today]
    omni_df = omni_df[["STUDENTID", "IDENTITYID", "SCHOOLENROLLDATE"]]
    return omni_df



tab1, tab2, tab3, tab4, tab5 = st.tabs(["BOY MAP Upload", "MOY MAP Upload", "Omni Report Upload", "Report Output", "Data Summary"])

st.sidebar.header("LSOA Map Rollup Report Creator")

# Upload BOY MAP Report
boy_map_file = st.sidebar.file_uploader("BOY Map Report file as Excel (.xlsx or .csv)", type=["xlsx", "csv"])
if boy_map_file:
    boy_df = process_boy_map_file(boy_map_file)
    tab1.dataframe(boy_df)
    st.sidebar.success("BOY MAP file successfully uploaded.")

# Upload MOY MAP Report
moy_map_file = st.sidebar.file_uploader("MOY Map Report file as Excel (.xlsx or .csv)", type=["xlsx", "csv"])
if moy_map_file:
    moy_df = process_moy_map_file(moy_map_file)
    tab2.dataframe(moy_df)
    st.sidebar.success("MOY MAP file successfully uploaded.")

# Upload Omni Report
omni_file = st.sidebar.file_uploader("Omni file as CSV (.xlsx or .csv)", type=["xlsx", "csv"])
if omni_file:
    omni_df = process_omni_file(omni_file)
    tab3.dataframe(omni_df)
    st.sidebar.success("Omni file successfully uploaded.")

# Merge and Data Summary
try:
    if tab4.button("Merge"):
        omni_df['STUDENTID'] = omni_df['STUDENTID'].astype(str)
        omni_df['IDENTITYID'] = omni_df['IDENTITYID'].astype(str)
        merged_df = omni_df.merge(boy_df, how="left", left_on="IDENTITYID", right_on="Student ID", indicator="_boy")
        merged_df = merged_df.merge(moy_df, how="left", left_on="IDENTITYID", right_on="Student ID",
                                    indicator="_moy")
        merged_df = merged_df[["STUDENTID", "BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed", "MOY MAP RLA",
                               "MOY MAP MATH", "MOY MAP Completed"]]
        merged_df.loc[(merged_df['BOY MAP Completed'] != "Yes") & (
                merged_df['BOY MAP Completed'] != "No"), ["BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed"]] = "N/A"
        merged_df.loc[merged_df['MOY MAP RLA'] == 'Language Arts', 'MOY MAP RLA'] = "Yes"
        merged_df.loc[merged_df['MOY MAP RLA'] != 'Yes', 'MOY MAP RLA'] = "No"
        merged_df.loc[merged_df['MOY MAP MATH'] == 'Mathematics', 'MOY MAP MATH'] = "Yes"
        merged_df.loc[merged_df['MOY MAP MATH'] != 'Yes', 'MOY MAP MATH'] = "No"
        merged_df.loc[
            (merged_df['MOY MAP RLA'] == "Yes") & (moy_df['MOY MAP MATH'] == "Yes"), 'MOY MAP Completed'] = "Yes"
        merged_df.loc[merged_df['MOY MAP Completed'] != 'Yes', 'MOY MAP Completed'] = "No"
        merged_df["EOY MAP RLA"] = ""
        merged_df["EOY MAP MATH"] = ""
        merged_df["EOY MAP Completed"] = ""
        tab4.dataframe(merged_df)
        
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
        tab5.dataframe(metrics_df)

except Exception as e:
    st.warning(f"Please upload both files above. Error: {e}")



