import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("add details")
st.markdown("enter the details below")

conn=st.experimental_connection("gsheets",type=GSheetsConnection)

existing_data=conn.read(worksheet="Sheet1",usecols=list(range(7)),ttl=5)
existing_data=existing_data.dropna(how="all")
st.dataframe(existing_data)
col1,col2,col3=st.columns(3)
col1.write("hi hello")
col2.write("welcome to")
col3.write("my website")
college_list=['Aditya university','aditya engineering college (AEC)','aditya college of engineering and technology (ACET)','aditya college of engineering (ACOE)']
dep_list=['CSE','ECE','EEE','MECH','CIVIL','AIML','IOT']
with st.form(key="new data"):
    name=st.text_input("enter your name *")
    father=st.text_input("enter your father's name")
    roll=st.text_input("enter your roll number *",max_chars=10,placeholder="only in caps")
    college=st.selectbox("Select your college",options=college_list)
    department=st.selectbox("Select your Department",options=dep_list)
    section=st.selectbox("Select your section",options=['A','B','C','D'])
    cgpa=st.text_input("enter your present SGPA *",max_chars=4)
    percentage=st.text_input("enter your percentage *",placeholder="prefer upto 2 decimals")
    feedback=st.text_area("Feedback",placeholder="please provide your feedback about the website it would be helpful")
    submit_button=st.form_submit_button("Submit")

    if submit_button:
        if not name or not roll or not cgpa or not percentage:
            st.warning("please enter the mandatory fields")
            st.stop()
        elif existing_data["roll number"].str.contains(roll).any():
            st.warning("the person with same roll number is existed")
            st.stop()
        else:
            add_data=pd.DataFrame(
                [
                   {
                       "name":name,
                       "father name": father,
                       "roll number": roll,
                       "college":college,
                       "department":department,
                       "section":section,
                       "cgpa":cgpa,
                       "percentage":percentage,
                       "feedback":feedback,
                   } 
                ]
            )
            update=pd.concat([existing_data,add_data],ignore_index=True)
            conn.update(worksheet="Sheet1",data=update)
            st.success("data submitted successfully")