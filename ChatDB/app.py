from click import prompt
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

#configuring api key
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


#Function to load Gemini Model
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([question,prompt[0]])
    return response.text

#Function to retrieve query from the SQL DB
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()

    #loop to print rows
    for row in rows:
        print(row)

    return rows



#Defining Prompt
prompt=[
    """
    You ar an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME,CLASS,SECTION and MARKS \n\n For Example 1- How many entries of 
    records are present in the STUDENT Table and the SQL Command will be something like this SELECT COUNT(*) FROM STUDENT;
    also the sql code should not have ``` in the begining or end and. you will only return the SQL query nothing else.
    """
]


#streamlit app
st.set_page_config(page_title="SpeakDB APP ", layout="wide")
st.header("Gemini App To Retrieve SQL Data")
question=st.text_input("input: ",key="input")

submit=st.button("Ask the Question")

