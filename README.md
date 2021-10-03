# Pirssi

Pirssi is a Python client for using IRC as a message broker.

Code itself does not require any external libraries, only tests and static analysis require installation of `requirements-test.txt`

## How this plays out

A publisher sends messages to an IRC channel which is a sort of message broker in this case. Every message is by default prefixed with `:pirssi:`, that's the queue information.

A consumer connects to given IRC channel and starts reading messages. It filters out every message except ones with the prefix. Messages are then forwarded to a handler.

Handler is simple implementation of a list of callable objects. It works by calling every object inside it with received argument.

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
$ python example.py consumer
```

And wait for the consumer to connect into channel. It produces a log line something like this.
```text
2021-10-03 10:46:59+0300 INFO pirssi.connection Connected to #pirssi-queue as pirssi-475e019b9354
```

Then start the publisher.
```shell
$ python example.py publisher
```

Publisher publishes few messages and then quits, consumer receives those and forwards them to a handler which prints them out.

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
$ pip install -r requirements-test.txt
```

Run tests using following command in project path.
```shell
$ python -m unittest -v
```

And finally run static analysis.
```shell
$ flake8
$ mypy ./
```
