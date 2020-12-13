# Antibot
## Description
Abtibot is a fully modular, easy to use and extensible Amino bot. It has never beenthis easy to add new skills to an Amino bot.
Built over the *slightly modified* Amino.py library, it is pretty straight forward to use right out of the box. You just need to remove the `security=False` inside `bot.py` for it to work. I wont remove it first, because I modified Amino.py to work that way. (you can always just use my fork of the library for that purpose.

## Get the bot
You need to run the following to get Antibot inside your computer:
```bash
git clone https://github.com/fredrare/Antibot.git
```

To get inside the Antibot's directory, run:
```bash
cd Antibot
```

## Usage
To start the bot, you need to run main.sh:
```bash
# Make sure Antibot is executable (just the first time)
chmod +x bot.py

# Install the requirements for the bot (also the first time)
pip install -r requirements.txt

# Export your account credentials to environment variables. Do not store them inside files!
# Do this every time you restart your terminal
export AMINO_USER="mail@example.com"
export AMINO_PASS="P4sSwor!d."

# Run Antibot
./bot.py

# To stop it, just hit ctrl+c
```

## Further improve the bot
If you want to add skills to the bot, you may create a directory or python file inside the `skills`directory.

### Creation
The file should have, at least, the following structure:
```python
skills = {
    'skillName': {
        'desc': 'Skill description',
        'run': callback
    }
}
```

The file should abide by these rules:

[ ] skillName: One-word name for the skill. It must be prefixed with '$' when invoked

[ ] callback: A function that:

  - Receives `data` (the data received by the event callback in Amino.py)
  - Returns a dictionary with the parameters you want for `subclient.send_message()`. Here, you **must** always include the `message`key.
  Example: 
```python
def callback(data):
    return {'message': 'Success!'}
```

### Tip
You may use the `common.util.skillable` decorator for your skill callbacks if you want to have context variables ready to use. If you wish to walk this path, you must add a second parameter `context` to the callback function. Example:
```python
from common.util import skillable

@skillable
def callback(data, context):
    return {'message': success, 'replyTo': context.origin}
```

More details of the accepted context attributes are available in `common.util.Context`.

### Inclusion
To use your recently created skill, you should import the file/directory inside the `skills/__init__.py` file. And then add it to `modules` in line 6.
```python
from skills import base, myNewSkill

modules = [base, myNewSkill]
```
And you are done.

## TODO
[ ] Add a man page for each skill.

[ ] Add a `'man'` key for each skill. The value will be displayed inside the man page.

[ ] Delete syntax information inside the help output.

[ ] Use a database instead of jsons for persistency.

[ ] Include `'mute'` and `'unmute'` skills for each chat.
