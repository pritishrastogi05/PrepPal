import json
import streamlit as st
from streamlit_lottie import st_lottie
import os
from apikey import api_key
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
# from langchain.document_loaders import PyPDFLoader
# from langchain.vectorstores import Chroma

# Defining our api key from chatgpt
os.environ['OPENAI_API_KEY']=api_key

llm = OpenAI(temperature=0.9)

subjects = ['Maths','Science','History','Civics','Geography','Economics']
grade = ['VIII','IX','X']
subject = []


def load_animation(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)


class define_static_parameters:
    def __init__(self,grade,subject,subjects):
        self.grade = grade
        self.subject = subject
        self.subjects = subjects

    def landing_page(self):
        st.title("PrepPal")
        icon=load_animation(os.path.join('app_media','waveforms.json'))
        st_lottie(icon,loop=True)
        st.write("Helping you prepare better")
        self.subjects = ['Maths','Science','History','Civics','Geography','Economics']
        self.grade = st.selectbox("Please choose your grade",options=['VIII','IX','X'])
        self.subject = st.selectbox("Please select subject",options=self.subjects)

    def subject_page(self):
        st.title(self.subject)
        Sylabus,Chapter,Explanations,Questions,Analysis = st.tabs(['Sylabus','Chapter','Explainers','Questions','Analysis'])
        with Sylabus:
            st.write(f'The sylabus for {self.grade} {self.subject} consists of-')
            input_variables = ['self.grade','self.subject']
            sylabus_prompt = f'what is the sylabus for CBSE {self.grade} {self.subject}?'

            response=(llm(sylabus_prompt))

            if sylabus_prompt:
                st.write(response)

        with Chapter:
            chapter_prompt = f'What are the chapters in CBSE {self.grade} {self.subject}?'
            response = llm(chapter_prompt)
            if chapter_prompt:
                st.write(response)

        with Explanations:
            list_prompt = f'Give me the chapters in CBSE {self.grade} {self.subject} as a python list without a variable name'
            list_response=llm(list_prompt)
            chapters = list_response.split(',')
            chapter = st.selectbox("Select a chapter", options=chapters)

            overview_prompt = f'Give me a brief overview of the CBSE Chapter-{chapter} for {self.grade} in {self.subject}'
            overview = llm(overview_prompt)
            st.title('Chapter Overview')
            st.write(overview)

            subtopics_prompt = f'What are the subtopics in {self.grade} {self.subject} {chapter}?'
            subtopics = llm(subtopics_prompt)
            st.title('Topics')
            topics = subtopics.split(',')
            for topic in topics:
                st.write(topic)

instance = define_static_parameters(grade=None,subject=None,subjects=None)
instance.landing_page()
instance.subject_page()