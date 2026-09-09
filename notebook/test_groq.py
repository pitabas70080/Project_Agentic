from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Find the .env file in the parent folder
env_path = Path(__file__).parent.parent / ".env"

# Load environment variables
load_dotenv(env_path)


# Create Groq model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# Send a simple message
response = llm.invoke(
    "Explain in one sentence what a goal-based agent is."
)


print(response.content)