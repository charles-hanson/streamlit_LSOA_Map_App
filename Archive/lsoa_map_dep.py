import streamlit as st
import pandas as pd
from datetime import date

boy_df = pd.read_csv('MapReport/boy.csv', dtype=str)
tab1, tab2, tab3, tab4 = st.tabs(["MAP Upload", "Omni Report Upload", "Report Output", "Data Summary"])

st.sidebar.header("LSOA Map Rollup Report Creator")

st.sidebar.subheader("➡️ Upload the MAP Report downloaded from the MAP website as an Excel file.")
try :

    map_file = st.sidebar.file_uploader("Map Report file as Excel (.xlsx)")

    map_df = pd.read_excel(map_file)
    map_df = map_df[["Student ID", "Subject"]]
    map_df['Student ID'] = map_df['Student ID'].astype(str)
    student_df = map_df.copy()
    student_df = student_df[["Student ID"]]
    student_df.drop_duplicates(subset=['Student ID'], inplace=True)
    rla_df = map_df.copy()
    rla_df = rla_df[rla_df["Subject"]=="Language Arts"]
    rla_df.rename(columns={'Subject':'MOY MAP RLA'}, inplace=True)
    mth_df = map_df.copy()
    mth_df = mth_df[mth_df["Subject"]=="Mathematics"]
    mth_df.rename(columns={'Subject':'MOY MAP MATH'}, inplace=True)
    # completion_df = student_df.merge(boy_df, how = "left", on="Student ID")
    completion_df = student_df.merge(rla_df, how = "left", on="Student ID")
    completion_df = completion_df.merge(mth_df, how="left", on="Student ID")
    completion_df['MOY MAP Completed'] = ""
    completion_df.loc[completion_df['MOY MAP RLA']=='Language Arts','MOY MAP RLA'] = "Yes"
    completion_df.loc[completion_df['MOY MAP RLA']!='Yes','MOY MAP RLA'] = "No"
    completion_df.loc[completion_df['MOY MAP MATH']=='Mathematics','MOY MAP MATH'] = "Yes"
    completion_df.loc[completion_df['MOY MAP MATH']!='Yes','MOY MAP MATH'] = "No"
    completion_df.loc[(completion_df['MOY MAP RLA']=="Yes") & (completion_df['MOY MAP MATH']=="Yes"), 'MOY MAP Completed'] = "Yes"
    completion_df.loc[completion_df['MOY MAP MATH']!='Yes','MOY MAP Completed'] = "No"
    tab1.dataframe(completion_df)
    st.sidebar.success("MAP file successfully uploaded.")
except:
    st.sidebar.warning("Please upload your MAP file.")

st.sidebar.subheader("➡️ Upload the Omni Report downloaded from the Oracle Report Server as a CSV file.")
try :
    omni_file = st.sidebar.file_uploader("Omni file as CSV (.csv)")
    
    omni_df = pd.read_csv(omni_file, dtype=str)
    omni_df = omni_df.loc[omni_df['SCHOOL']==("Lone Star Online Academy @ Roscoe")]
    omni_df['SCHOOLENROLLDATE'] = pd.to_datetime(omni_df['SCHOOLENROLLDATE']).dt.date
    today = date.today()
    omni_df = omni_df[omni_df['SCHOOLENROLLDATE'] <= today]
    omni_df = omni_df[["STUDENTID", "IDENTITYID","SCHOOLENROLLDATE"]]
    tab2.dataframe(omni_df)
    st.sidebar.success("Omni file successfully uploaded.")
except:
    st.sidebar.warning("Please upload your Omni file.")

tab3.write("👆 Click Merge below to complete the cleaning process.")
try :
    if tab3.button("Merge"):
        merged_df = omni_df.merge(boy_df, how = "left", left_on="STUDENTID", right_on = "Student ID", indicator = "_boy")
        merged_df = merged_df.merge(completion_df, how = "left", left_on="IDENTITYID", right_on="Student ID", indicator="_merged")
        merged_df = merged_df[["STUDENTID", "BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed", "MOY MAP RLA", "MOY MAP MATH", "MOY MAP Completed"]]
        merged_df.loc[(merged_df['BOY MAP Completed']!="Yes") & (merged_df['BOY MAP Completed']!= "No") , ["BOY MAP RLA", "BOY MAP MATH", "BOY MAP Completed"]] = "N/A"
        merged_df.loc[merged_df['MOY MAP RLA']=='Language Arts','MOY MAP RLA'] = "Yes"
        merged_df.loc[merged_df['MOY MAP RLA']!='Yes','MOY MAP RLA'] = "No"
        merged_df.loc[merged_df['MOY MAP MATH']=='Mathematics','MOY MAP MATH'] = "Yes"
        merged_df.loc[merged_df['MOY MAP MATH']!='Yes','MOY MAP MATH'] = "No"
        merged_df.loc[(merged_df['MOY MAP RLA']=="Yes") & (completion_df['MOY MAP MATH']=="Yes"), 'MOY MAP Completed'] = "Yes"
        merged_df.loc[merged_df['MOY MAP Completed']!='Yes','MOY MAP Completed'] = "No"

        tab3.dataframe(merged_df)

except : 
    st.warning("Please upload both files above")
    

# tab4.selectbox("Pick one", ["BOY", "MOY"])
try :
    col1, col2, col3, col4, col5 = st.columns([1.75,1.75,2,1.75,2])
    col1.subheader("Metrics", divider = "rainbow")
    col1.write("Yes")
    col1.write("No")
    col1.write("N/A")
    col1.write("Total")
    col2.subheader("BOY Map #", divider = "rainbow")
    col3.subheader("BOY Map %", divider = "rainbow")
    col4.subheader("MOY Map #", divider = "rainbow")
    col5.subheader("MOY Map %", divider = "rainbow")


except :
    pass
    

    
st.metric("Total", 42,2)
st.metric("Total2",52,2)
             