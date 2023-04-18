"""Ein simpler slack bot, der deutsch spricht und einen lokalen vectorstore nutzt"""
import pickle
import os
from pathlib import Path
import langchain
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.cache import InMemoryCache
from dotenv import load_dotenv

langchain.llm_cache = InMemoryCache()

load_dotenv()


if not Path("embedded_docs.pkl").exists():
    raise ValueError("embedded_docs.pkl existiert nicht, "
                     "bitte führen Sie zunächst 'python import.py' aus")
with open("embedded_docs.pkl", "rb") as f:
    vectorstore = pickle.load(f)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", default="")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"

OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", default="gpt-3.5-turbo")
assert OPENAI_API_MODEL, "OPENAI_API_MODEL environment variable is missing from .env"

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", default="")
assert SLACK_BOT_TOKEN, "SLACK_BOT_TOKEN environment variable is missing from .env"

SLACK_BOT_KEYWORD = os.getenv("SLACK_BOT_KEYWORD", default="documentbot")
assert SLACK_BOT_KEYWORD, "SLACK_BOT_KEYWORD environment variable is missing from .env"

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", default="")
assert SLACK_APP_TOKEN, "SLACK_APP_TOKEN environment variable is missing from .env"


llm = OpenAI(
    temperature=0.1,
    model_name=OPENAI_API_MODEL,
)

GERMAN_CONDENSE_PROMPT = """
Gegeben die folgende Unterhaltung und eine anschliessende Frage, 
formuliere die Folgefrage als eigeneständige Frage um.

Unterhaltung:
{chat_history}
Folgefrage: {question}
Eigenständige Frage:"""

condense_prompt = PromptTemplate.from_template(GERMAN_CONDENSE_PROMPT)

# german template for question prompt
GERMAN_PROMPT = """
Verwende die folgenden Kontextinformationen, um die Frage am Ende zu beantworten. 
Wenn du die Antwort nicht weißt, sag einfach, dass du es nicht weißt und versuche nicht, eine Antwort zu erfinden.

{context}

Frage: {question}
Hilfreiche Antwort:"""

qa_prompt = PromptTemplate(
    template=GERMAN_PROMPT, input_variables=["context", "question"]
)

# Die eigentliche QA-Chain
qa_chain = ChatVectorDBChain.from_llm(
    llm,
    vectorstore,
    qa_prompt=qa_prompt,
    condense_question_prompt=condense_prompt,
)
history = []

app = App(
    token=SLACK_BOT_TOKEN,
)

@app.message(SLACK_BOT_KEYWORD)
def message_hello(message, say):
    """Frage an openai, Ergebnis an user"""
    question = message['text'].replace(SLACK_BOT_KEYWORD,'')
    answer = qa_chain({"question":question, "chat_history": history})['answer']
    say(
        text=f"<@{message['user']}>: {answer}"
    )
    history.append((question, answer))

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
