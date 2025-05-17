# discord_util.py – Minimaler Stub für discord.py (Mock-Client)

class Client:
    def __init__(self, *args, **kwargs):
        self.user = None

    async def start(self, *args, **kwargs):
        print("🧪 Stub-Client gestartet")

    async def close(self):
        print("🧪 Stub-Client geschlossen")

    def run(self, token):
        print(f"🧪 run(token={token}) aufgerufen (stub)")

    def is_ready(self):
        return True


class Intents:
    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def all(cls):
        return cls()


class Message:
    def __init__(self, content="", author=None):
        self.content = content
        self.author = author


class User:
    def __init__(self, name="StubUser"):
        self.name = name
        self.id = 1234
