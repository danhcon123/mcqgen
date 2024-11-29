import json
import os
import pandas as pd
import traceback
import PyPDF2
from dotenv import load_dotenv
from .utils import read_file, get_table_data
from .logger import logging

#importing necessary packages from langchain
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain.chains import SequentialChain, LLMChain
from langchain_community.callbacks import get_openai_callback

#load environment variables from .env file
load_dotenv()

#Acces the env variables just like you would with os.environment
#Define LLM
#openai_api_key = ""
key=os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(openai_api_key=key, model_name = "gpt-3.5-turbo", temperature=0.7)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions
for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs
###RESPONSE_JSON
{responses_json}
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "responses_json"],
    template=TEMPLATE
)



TEMPLATE_2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use at max 50 words for complexity
if the quiz is not at per with the cognitive and analytical abilities of the students, \
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert in English Writer of the above quiz:
"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE_2)


'''quiz_chain = quiz_generation_prompt | llm
#quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

review_chain = quiz_evaluation_prompt | llm
#review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True )

#Create chain sequence
generate_evaluation_chain= quiz_chain | quiz_evaluation_prompt
'''
# Create LLM chains for quiz generation and evaluation
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Combine them into a sequential chain
generate_evaluation_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "responses_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
#Token usage tracking
#How to setup Token usage Tracking in Langchain
#Use this to calculate the token and the cost of input and generated output tokens through OPEN AI API
# No money -> No result. Sr. This is how OpenAI works


'''

TEXT = "Sample text for generating MCQs."
NUMBER = 5
SUBJECT = "Mathematics"
TONE = "formal"
RESPONSE_JSON = {"questions": [
    {"question" : "", "options" : ["", "", "", ""], "answer": ""}
    ]
}

# Token usage tracking
with get_openai_callback() as cb:
    response=generate_evaluation_chain.invoke(
        {
            "text": TEXT,
            "number": NUMBER,
            "subject":SUBJECT,
            "tone":TONE,
            "responses_json": json.dumps(RESPONSE_JSON)
        }
    )
    print("Token usage:", cb)
'''