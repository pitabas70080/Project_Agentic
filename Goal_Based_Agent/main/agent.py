from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool, AgentType
from dotenv import load_dotenv
import os
import re

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
)