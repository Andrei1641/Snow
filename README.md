# Game Snow

---

## The course of the game

Objects of different shapes fall downward. The player’s goal is to hit them; each successful hit awards points.
The objects have various, so to speak, mutations that allow them to dodge the player’s cursor.
The harder an object is to hit, the more points it gives.
If the player misses an object, another one is added to the game,
making it more difficult—but now each object yields more points (with a multiplier).

## Statistic
At the end of the game, the statistics will be displayed: the first-place score, your score, and your ranking.

To compete with other players, you can connect to a server or create your own.
To do this, you need to create a <code>.env</code> file with the following variables:

```dotenv
DB_PASSWORD=<password>
DB_NAME=<db name>
HOST=<host>
USER=<user>
```

## Required packages for the game

To install the required packages for the game, enter:
```bash
py -m pip install -r requirements.txt
```