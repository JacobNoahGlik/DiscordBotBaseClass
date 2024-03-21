import discord
import collections
from typing import Callable

class DiscordBot:
    def __init__(self, invite_link: str, token: str, max_memory: int = 10):
        self._caught_msgs: collections.deque = collections.deque(maxlen=max_memory)
        self._sent_msgs: collections.deque = collections.deque(maxlen=max_memory)
        self._all_msgs: collections.deque = collections.deque(maxlen=max_memory)
        self._commands = dict()
        self._asign_to_self_helper(invite_link, token)
        self._set_client()
        self._set_events()
        self._ready_function = DiscordBot.generate_default_ready_function()
        self._on_message = DiscordBot.generate_default_on_message_function()
    def _asign_to_self_helper(self, invite_link, token) -> None:
        self._invite_link: str = invite_link
        self._token: str = token
        self._ignore_on_atMention: bool = False
        self._on_atMention = DiscordBot.generate_default_on_atMention_example()
    def _set_client(self, access_message_content:bool = True) -> None:
        self._intents: discord.Intents = discord.Intents.default()
        if access_message_content: 
            self._intents.message_content = True
        self._client: discord.Client = discord.Client(intents=self._intents)
    def _set_events(self) -> None:
        @self._client.event
        async def on_ready():
            if self._ready_function:
                await self._ready_function(self)
        @self._client.event
        async def on_message(message):
            self._all_msgs.append(message)
            if message.author == self._client.user:
                self._sent_msgs.append(message)
                return
            self._caught_msgs.append(message)
            await self._on_ated(message)
            if self._on_message:
                await self._on_message(self, message)
            await self._run_commands(message)
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
    def get_last_message(self) -> discord.Message | None:
        if len(self._caught_msgs) == 0:
            return None
        return self._caught_msgs[-1]
    def get_last_total_message(self) -> discord.Message | None:
        if len(self._all_msgs) == 0:
            return None
        return self._all_msgs[-1]
    def set_on_message_function(self, function) -> None:
        self._on_message = function
    def get_id(self) -> int | None:
        return self._client.user.id if self._client.user else None
    def get_global_name(self) -> str | None:
        return self._client.user.global_name if self._client.user else None
    def set_ready_function(self, function) -> None:
        self._ready_function = function
    async def _on_ated(self, message: discord.Message) -> None:
        if not self._ignore_on_atMention and f'<@{self.get_id()}>' in message.content and self._on_atMention:
            await self._on_atMention(self, message)
    def set_on_atMention_function(self, function) -> None:
        self._on_atMention = function
    def ignore_atMention(self) -> None:
        self._ignore_on_atMention = True
    async def reply(self, content, mention:bool = True) -> Exception | None:
        try:
            if self._caught_msgs[-1]:
                await self._caught_msgs[-1].reply(content, mention_author=mention)
                return None
        except Exception as e:
            return e
    def self_mention(self) -> str:
        return f'<@{self.get_id()}>'
    def author_mention(self, message: discord.Message | None = None) -> str:
        if message:
            return f'<@{message.author.id}>'
        if len(self._caught_msgs) > 0:
            return f'<@{self._caught_msgs[-1].author.id}>'
        return ''
    async def _run_commands(self, message: discord.Message):
        for key, value in self._commands.items():
            if message.content.startswith(key):
                await value(self, message)
    def on_command(self, command: str, function) -> None:
        self._commands[command] = function
    def set_commands(self, commands: dict[str, Callable]) -> None:
        self._commands = commands
    def add_commands(self, commands: dict[str, Callable]) -> None:
        self._commands.update(commands)
    def run(self) -> None:
        try:
            self._client.run(self._token)
        except discord.errors.LoginFailure as e:
            print('Function: DiscordBot.run()')
            print(f'\tCAUGHT A TOKEN ERROR: Token "{self._token}" has expired or isn\'t valid.\n\t\tOriginal err: {e.__repr__()}\n\t\tError Type:   "discord.errors.LoginFailure"')
        except discord.errors.ConnectionClosed as e:
            print('Session ended unexpectedly with error code:')
            print(e.__repr__())
    @staticmethod
    def generate_default_ready_function() -> Callable:
        async def default_ready_function(self: DiscordBot) -> None:
            print(f'We have logged in as {self._client.user}')
        return default_ready_function
    @staticmethod
    def generate_default_on_message_function() -> Callable:
        async def default_on_message_function(self: DiscordBot, message: discord.Message) -> None:
            print(f'Got message: "{message.content}" from user "{message.author}"')
        return default_on_message_function
    def generate_default_on_atMention_example() -> Callable:
            async def on_atMention_example(self: DiscordBot, message: discord.Message) -> None:
                print('I was mentioned!')
                await self.reply('I was mentioned!', True)
            return on_atMention_example
  

def example_bot():
    # get join link and token for bot
    from config import join_link, token

    # define on message function
    async def on_message(self: DiscordBot, message: discord.Message):
        print(f'Got message: "{message.content}" from user "{message.author}"')

    # define on mention functon
    async def on_mention(self: DiscordBot, message: discord.Message):
        print('I was mentioned!')
        msg = f'{self.author_mention(message)} @-ed me!'
        print(f'{msg=}')
        await self.reply(msg)
        
    # define a command
    async def tell_a_joke(self: DiscordBot, message: discord.Message):
        pre_joke: str = f"This one's for {self.author_mention(message)}:\n"
        joke: str = 'Why did the chicken cross the road? To get to the other side!'
        await self.reply(pre_joke + joke)
        print(f'Told a joke to {message.author}')

    # create the bot
    test: DiscordBot = DiscordBot(join_link, token)

    # set the functions
    test.set_on_message_function(on_message)
    test.set_on_atMention_function(on_mention)
    test.on_command('/joke', tell_a_joke)

    # run the bot
    test.run()


def main():
    print("""Test Bot is a test discord bot that will:
    1. Log each discord message
    2. Reply to messages where it is @mention-ed
    3. Tell a joke when the `/joke` command is used
    
Running Test Bot...""")
    example_bot()
        
if __name__ == '__main__':
        main()
    