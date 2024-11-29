# Pirssi

[![Tests](https://github.com/wonkybream/pirssi/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/wonkybream/pirssi/actions/workflows/tests.yml)

Pirssi is a Python client for using IRC as a message broker.

Code itself does not require any external libraries, only static analysis require installation of `requirements.txt`.

## How this plays out

A publisher sends messages to an IRC channel which is a sort of message broker in this case. Every message is by default prefixed with `:pirssi:`, that's the message queue information.

A consumer connects to the given IRC channel and starts consuming messages. The consumer filters out every message except ones with the prefix. Messages are then forwarded to a handler.

Handler is simple implementation of a list of callable objects. The handler works by calling every object inside it with received argument.

```python
from pirssi.handler import Handler

def handler_function(message: str):
    print(f"Handling message: {message}")

handler = Handler()

# Append handler function
handler.append(handler_function)

# Call handler
handler("Some information")
```

Output: `Handling message: Some information`


## Running example

Both consumer and publisher need to be run separately.

If you want to see how this all plays out. https://webchat.quakenet.org/ is excellent for monitoring channel communications.
The default channel is `#pirssi-queue`.

At first start the consumer.
```shell
python example.py consumer
```

And wait for the consumer to connect into channel. the consumer produces a log line something like this.
```text
2021-10-03 10:46:59+0300 INFO pirssi.connection Connected to #pirssi-queue as pirssi-475e019b9354
```

Then start the publisher.
```shell
python example.py publisher
```

The publisher publishes few messages and then quits, the consumer receives those messages and forwards them to a handler which prints them out.

Looking from https://webchat.quakenet.org/, communication looks closely following.
```text
[10:46] == pirssi-475e019b [~pirssi-47@xxxx] has joined #pirssi-queue
[10:47] == pirssi-81a725a2 [~pirssi-81@xxxx] has joined #pirssi-queue
[10:47] <pirssi-81a725a2> :pirssi:{"message": "I command you to do something"}
[10:47] <pirssi-81a725a2> :pirssi:{"message": "I would like to query some information"}
[10:47] <pirssi-81a725a2> :pirssi:{"message": "Something weird happened and you should know about it"}
[10:47] == pirssi-81a725a2 [~pirssi-81@xxxx] has quit [Quit]
[10:47] == pirssi-475e019b [~pirssi-47@xxxx] has quit [Quit]
```


## Running tests

Project uses Python unittest as a testing framework, flake8 as style checker and mypy as a type checker.

Install test requirements.
```shell
pip install -r requirements.txt
```

Run tests using following command in the project path.
```shell
python -m unittest -v
```

Or run everything at once.
```shell
./scripts/precommit.sh
```
