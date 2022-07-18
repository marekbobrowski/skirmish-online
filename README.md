# Skirmish Online

Skrimish Online is a base for a multiplayer ([MMORPG](https://en.wikipedia.org/wiki/Massively_multiplayer_online_role-playing_game) style) game, written in [Python](https://www.python.org/) with [Panda3D](https://www.panda3d.org/). It uses client-server model, with server and it's memory ([Redis](https://redis.io/)) being ran in a [docker](https://www.docker.com/) container.

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

The server detects timeouts and removes players who actually left the game.

## Screenshots and videos

Here are some screenshots and a video showing current state of the project.

## Setting up the project

Make sure you have [Python](https://www.python.org/) and [Docker](https://www.docker.com/) installed.
Open the project directory.

1. `pip install -r requirements.txt` to install all dependencies,
2. `docker compose build server` to build the docker image,
3. `docker compose up` to run the server and memory app (redis),
4. `python -m client` to run the client.

## Documentation (for future me)

#### Adding new message that can be sent between server and clients.
