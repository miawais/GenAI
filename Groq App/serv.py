
#Importing Required Libraries 

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os 
from langserve import add_routes 
from dotenv import load_dotenv
load_dotenv()

#importing Groq API 
groq_api_key=os.getenv("GROQ_API_KEY")

#Importing Model 
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)



#1.Create Prompt Template 
system_template="Translate the following into {language}:"
prompt_template=ChatPromptTemplate.from_messages(
    [("system",generic_template),
    ("user","{text}")
    ]
)

parser=StrOutputParser()


#2.Creating Chain 
chain=prompt_template|model|parser


#App Defination 
app=FastAPI(title="LangChainServer",
            version="1.0",
            description="Simple Langchain APP")



#Adding Chain Routes 
add_routes(
    app,
    chain,
    path="/chain"
)



if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)