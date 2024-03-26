# Everything You Need to Know About the Bot Python File

<br>

[Link to discord's developer portal](https://discord.com/developers/application)

<br>

# DiscordBot Class
Turining the python code for discord bots into class structures instead of script style code

<br>

## `class::DiscordBot` Abilities
* Ability to know if it was mentioned
* Ability to recognize custom commands and execute saved functions based on those commands

<br>

## `class::DiscordBot` Functions:
Initialization + static methods
* `__init__(self, invite_link: str, token: str, max_memory: int = 10):`
  * Initialize a new DiscordBot Object
  * `invite_link` (type `str`) is the string used to invite your bot to a server
  * `token` (type `str`) is the token needed to run your bot
  * `Max_memory` *OPTIONAL*  (type `int`) is the maximum previous messages the bot will remember
    * If a new message comes in and there are already 10 saved, it will replace the oldest one
  * `custom_intents` *OPTIONAL*  (type `discord.Intents`) is an optional custom intent that will be applied to the DiscordBot client (type `discord.Client`) and will override the default intents which are only those needed to access the messages. 
    * The default `discord.Intent` is defined as `discord.Intents.default().message_content = True`.
* `@staticmethod`  `def generate_default_ready_function() -> Callable:`
  * Generate the default `on_ready` function for the bot.
    * An `on_ready` function will run every time the bot comes online.
    * An `on_ready` function will run with `self` (the `DiscordBot` object) as input.
    * Any `return`/output from an `on_ready` function is ignored.
  * No input expected for this function.
  * Returns a function (`typing.Callable`) object
    * Which takes an input "self" of type `class::DiscordBot`
    * And returns `None` when called
* `@staticmethod`  `def generate_default_on_message_function() -> Callable:`
  * Generate the default `on_message` function for the bot.
    * An `on_message` function will run every time a message (not sent by the bot) is registered from DMs to any channel in any server that the bot is added to.
    * An `on_message` function will run with `self` (the `DiscordBot` object) and `message` (the `discord.Message`) that triggared this function call.
    * Any `return`/output from an `on_message` function is ignored.
  * No input expected for this function.
  * Returns a function (`typing.Callable`) object
    * Which takes two inputs "self" of type `class::DiscordBot` and "message" of type `class::discord.Message`
    * And returns `None` when called
* `@staticmethod`  `def generate_default_on_atMention_example() -> Callable:`

# Counter Class
Making counting and saving `discord.Messages` esier and more readable

<br>

## `class::Counter` Functions:
Initialization
* `__init__(self, max_memory: int):`
  * Initialize a new Counter object
  * Consists of 3 `collections.deque` containers which are limited in size using the `input::max_memory` value. (must be greator then zero)
  * Consists of 3 counters (type `int`) that will count total messages (recieved, sent, and total), ignoring the number of messages saved in counter as those are limited by the `input::max_memory` value

<br>

## `class::Counter` Member Functions:
* `add_my_message(self, increase: discord.Message):`
* `add_other_message(self, increase: discord.Message):`
* `get_my(self) -> collections.deque:`
* `get_other(self) -> collections.deque:`
* `get_total(self) -> collections.deque:`
* `get_my_msg_count(self) -> int:`
* `get_other_msg_count(self) -> int:`
* `get_total_msg_count(self) -> int:`
