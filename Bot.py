from types import FunctionType
import discord
import collections
from config import token, join_link

class DiscordBot:
    def __init__(self, invite_link, token, max_memory=10):
        self._caught_msgs = collections.deque(maxlen=max_memory)
        self._sent_msgs = collections.deque(maxlen=max_memory)
        self._asign_to_self_helper(invite_link, token)
        self._set_client()
        self._set_events()
        self._ready_function = DiscordBot.generate_default_ready_function(self._client.user)
        self._on_message = DiscordBot.generate_default_on_message_function()
    def _asign_to_self_helper(self, invite_link, token) -> None:
        self._invite_link = invite_link
        self._token = token
    def _set_client(self, access_message_content:bool =True) -> None:
        self._intents = discord.Intents.default()
        if access_message_content: 
            self._intents.message_content = True
        self._client = discord.Client(intents=self._intents)
    def _set_events(self) -> None:
        @self._client.event
        async def on_ready():
            if self._ready_function:
                await self._ready_function(self)
        @self._client.event
        async def on_message(message):
            if message.author == self._client.user:
                self._sent_msgs.append(message)
                return
            self._caught_msgs.append(message)
            if self._on_message:
                await self._on_message(self, message)
    def add_msg(self, msg) -> None:
        self._caught_msgs.append(msg)
    def get_messages(self) -> collections.deque:
        return self._caught_msgs
    def get_sent_messages(self) -> collections.deque:
        return self._sent_msgs
    def get_invite(self) -> str:
        return self._invite_link
    def get_token(self) -> str:
        return self._token
    def set_token(self, token: str) -> None:
        self._token = token
    def get_client(self) -> discord.Client:
        return self._client
    def get_last_message(self) -> discord.Message:
        return self._caught_msgs[-1]
    def set_on_message_function(self, function) -> None:
        self._on_message = function
    def get_id(self) -> int | None:
        return self._client.user.id if self._client.user else None
    def get_global_name(self) -> str | None:
        return self._client.user.global_name if self._client.user else None
    def set_ready_function(self, function) -> None:
        self._ready_function = function
    async def reply(self, content, mention:bool = True) -> Exception | None:
        try:
            if self._caught_msgs[-1]:
                await self._caught_msgs[-1].reply(content, mention_author=mention)
                return None
        except Exception as e:
            return e
    def get_self_mention(self) -> str:
        return f'<@{self.get_id()}>'
    def run(self) -> None:
        try:
            self._client.run(self._token)
        except discord.errors.LoginFailure as e:
            print('Function: DiscordBot.run()')
            print(f'\tCAUGHT A TOKEN ERROR: Token "{self._token}" has expired or isn\'t valid.\n\t\tOriginal err: {e.__repr__()}\n\t\tError Type:   "discord.errors.LoginFailure"')
    @staticmethod
    def generate_default_ready_function(user):
        async def default_ready_function(self: DiscordBot) -> None:
            print(f'We have logged in as {self._client.user}')
        return default_ready_function
    @staticmethod
    def generate_default_on_message_function():
        async def default_on_message_function(self: DiscordBot, message: discord.Message) -> None:
            print(f'Got message: "{message.content}" from user "{message.author}"')
        return default_on_message_function
        


            

    

def example_bot():
    test = DiscordBot(join_link, token)
    async def on_message(self, message):
        print(f'Got message: "{message.content}" from user "{message.author}"')
        if self.get_self_mention() in message.content:
            msg = 'You @-ed me!'
            print(f'{msg=}')
            await self.reply(msg)
    test.set_on_message_function(on_message)
    test.run()
    
            