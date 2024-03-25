# Everything You Need to Know About the Bot Python File

<br>

# DiscordBot Class
Turining the python code for discord bots into class structures instead of script style code

<br>

## `class::DiscordBot` Functions:
Initialization + static methods
* `__init__(self, invite_link: str, token: str, max_memory: int = 10):`
  * Initialize a new DiscordBot Object
  * `invite_link` (type `str`) is the string used to invite your bot to a server
  * `token` (type `str`) is the token needed to run your bot
  * `Max_memory` *OPTIONAL*  (type `int`) is the maximum previous messages the bot will remember
    * If a new message comes in and there are already 10 saved, it will replace the oldest one
* `@staticmethod`  `def generate_default_ready_function() -> Callable:`
  * Generate the default `on_ready` function for the bot.
    * An `on_ready` function will run every time the bot comes online
  * No input expected
  * Returns a function (`typing.Callable`) object
    * Which takes an input "self" of type `class::DiscordBot`
    * And returns `None` when called
* `@staticmethod`  `def generate_default_on_message_function() -> Callable:`
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
