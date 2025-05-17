
from langchain.tools import Tool

def get_event_tool():
    def fn(input): return f"Event created: {input}"
    return Tool(name="create_event", func=fn, description="Create a new event")
