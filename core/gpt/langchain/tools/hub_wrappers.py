
def wrap_tool(tool):
    return {
        "name": tool.name,
        "description": tool.description,
        "run": lambda x: tool.func(x)
    }
