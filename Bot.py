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
    def _asign_to_self_helper(self, invite_link, token):
        self._invite_link = invite_link
        self._token = token
    def _set_client(self, access_message_content:bool =True) -> discord.Client:
        self._intents = discord.Intents.default()
        if access_message_content: 
            self._intents.message_content = True
        self._client = discord.Client(intents=self._intents)
    def _set_events(self):
        @self._client.event
        async def on_ready():
            if self._ready_function:
                await self._ready_function(self)
        @self._client.event
        async def on_message(message):
            if message.author == client.user:
                self._sent_msgs.append(message)
                return
            self._caught_msgs.append(message)
            if self._on_message:
                await self._on_message(self, message)
    def add_msg(self, msg):
        self._caught_msgs.append(msg)
    def get_messages(self):
        return self._caught_msgs
    def get_sent_messages(self):
        return self._sent_msgs
    def get_invite(self):
        return self._invite_link
    def get_token(self):
        return self._token
    def set_token(self, token):
        self._token = token
    def get_client(self):
        return self._client
    def get_last_message(self):
        return self._caught_msgs[-1]
    def set_on_message_function(self, function):
        self._on_message = function
    def get_id(self):
        return self._client.user.id if self._client.user else None
    def get_global_name(self):
        return self._client.user.global_name if self._client.user else None
    def set_ready_function(self, function):
        self._ready_function = function
    async def reply(self, content, mention:bool = True): # -> Exception,None:
        try:
            if self._caught_msgs[-1]:
                self._caught_msgs[-1].reply(content, mention_author=mention)
                return None
        except Exception as e:
            return e
    def run(self):
        try:
            self._client.run(self._token)
        except discord.errors.LoginFailure as e:
            print('Function: DiscordBot.run()')
            print(f'\tCAUGHT A TOKEN ERROR: Token "{self._token}" has expired or isn\'t valid.\n\t\tOriginal err: {e.__repr__()}\n\t\tError Type:   "discord.errors.LoginFailure"')
    @staticmethod
    def generate_default_ready_function(user):
        async def default_ready_function(self):
            print(f'We have logged in as {self._client.user}')
        return default_ready_function
    @staticmethod
    def generate_default_on_message_function():
        async def default_on_message_function(self, message):
            print(f'Got message: "{message.content}" from user "{message.author}"')
        return default_on_message_function
        
    

    

def example_bot():
    test = DiscordBot(join_link, token)
    print(test.get_id())
    print(test.get_global_name())
    test.run()
    
            