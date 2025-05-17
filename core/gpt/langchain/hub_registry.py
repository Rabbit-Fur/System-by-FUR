
from langchainhub import pull

def get_tool(name: str):
    return pull(f"fur-system/{name}")
