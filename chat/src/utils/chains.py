import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import summary_model
from langchain_core.prompts import ChatPromptTemplate
from core.prompts import INTERVIEW_PROMPT, SUMMARY_PROMPT

def get_Summary_Model():
    model = summary_model()
    prompt = ChatPromptTemplate.from_messages([

        ("system",SUMMARY_PROMPT),
        ("human","{message]}")

    ])

    return prompt | model

    