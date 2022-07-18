# Skirmish Online

Skrimish Online is a base for a multiplayer, online game ([MMORPG](https://en.wikipedia.org/wiki/Massively_multiplayer_online_role-playing_game) style), written in [Python](https://www.python.org/) with [Panda3D](https://www.panda3d.org/). It uses client-server model, with server and it's memory ([Redis](https://redis.io/)) being ran in a [docker](https://www.docker.com/) container.

## Game description

Currently, player can do few things after connecting to the game server:
- run around on the map,
- chat with other players,
- use different abilities that deal damage to other players,
- change their character's model (text command),
- change their character's weapon model (text command),
- change their nickname (text command).

Every player has:
- health points that are subtracted when somebody attacks the player; they're restored over time
- mana points that are consumed when the player uses an ability; they're restored over time

All of these things are being constantly synchronized between server and all connected clients.

The server detects timeouts and removes players who left the game.

## Screenshots and videos

Here are some screenshots and a video showing current state of the project.

<img src="https://raw.githubusercontent.com/marekbobrowski/skirmish-online/master/screenshots/1.png">
<img src="https://raw.githubusercontent.com/marekbobrowski/skirmish-online/master/screenshots/2.png">

## Setting up the project

### Client usage only

Make sure you have [Python](https://www.python.org/) installed. Open the project directory.

1. `pip install -r client-requirements.txt` to install all client dependencies,
2. `python -m client <server IP without brackets>` to run the client.

### Client and server usage

Make sure you have [Python](https://www.python.org/) and [Docker](https://www.docker.com/) installed.
Open the project directory.

1. `pip install -r requirements.txt` to install all dependencies,
2. `docker compose build server` to build the docker image,
3. `docker compose up` to run the server and memory app (redis),
4. `python -m client <server IP without brackets, default is localhost>` to run the client.


## Client Development Manual

This section contains instructions on developing the most important parts of the client.

### Adding new GUI elements

The GUI package is located in `client/local/section/main/ui`. That's the place where you can create new class/package for some new GUI element. The file with main class `MainSectionUi` that stores all the GUI elements is called `ui.py`. Following the existing examples attach instance of your new class. If you want your GUI element to be in a fixed position on the screen (i. e. not connected with the 3D world) you will most probably want to pass `self.node` as an argument to your new class (this requires understanding of how [scene graph in Panda3D](https://docs.panda3d.org/1.10/python/programming/scene-graph/index) works). If you want your GUI elements to be connected to the 3D world (most propably player units), you want to pass self.model and then take care of reparenting GUI elements to the units (see `floating_bars.py` as a guide).

Most of the time, UI will update based on the events that were firstly received from the server and then "interpreted" by the client. In `client/event.py` there is a list of those events. In order to make your class respond to chosen events, you need to inherit from `direct.showbase.DirectObject.DirectObject` (Panda3D class) and import all events from `client.event.Event`. Then simply in init method write `self.accept(Event.<some event>, self.event_handler_method)` and in the specified method handle the event by updating your GUI element (you can check verious examples of that in all of the existing GUI classes). In order to know what event arguments are passed with the event, you need to check the place they are called. But for example, with event `UNIT_NAME_UPDATED`, there are passed 2 arguments: unit instance and the unit's old name.

### Create new type of message that can be sent between clients and server

Yet to be written about.

### Sending new type of message from client to server

In order to create some new kind of information that will be sent to the server, you need to create a new class inside `client/net/message_sender/senders` package and inherit from `BaseSender`. Specify the managed Event in the `MANAGED_EVENT` class field and the Message type it's going to send in `MESSAGE_CLS` class field (look at the existing examples in the `senders` package). Then "somewhere in the client" call specified event with proper arguments and data should be sent to the server.

### Handling new type of message sent by the server

Yet to be written about.

## Server Development Manual

Yet to be written about.



