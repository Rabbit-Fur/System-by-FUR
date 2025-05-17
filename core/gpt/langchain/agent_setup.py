
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

def setup_agent(tools):
    return initialize_agent(
        tools=tools,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=ConversationBufferMemory(),
        verbose=True,
        llm=ChatOpenAI(temperature=0)
    )
