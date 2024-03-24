# Everything You Need to Know About the Bot Python File

<br>

# DiscordBot Class
Turining the python code for discord bots into class structures instead of script style code

<br>

## `class::DiscordBot` Functions:
Initialization + static methods
* __init__(self, invite_link: str, token: str, max_memory: int = 10):
  * Initialize a new DiscordBot Object
  * `invite_link` (type `str`) is the string used to invite your bot to a server
  * `token` (type `str`) is the token needed to run your bot
  * `Max_memory` *OPTIONAL*  (type `int`) is the maximum previous messages the bot will remember
    * If a new message comes in and there are already 10 saved, it will replace the oldest one
* @staticmethod  def generate_default_ready_function() -> Callable:
  * Generate the default `on_ready` function for the bot.
    * An `on_ready` function will run every time the bot comes online
  * No input expected
  * Returns a function (`typing.Callable`) object
    * Which takes an input "self" of type `class::DiscordBot`
    * And returns `None` when called
* @staticmethod  def generate_default_on_message_function() -> Callable:
* @staticmethod  def generate_default_on_atMention_example() -> Callable:
