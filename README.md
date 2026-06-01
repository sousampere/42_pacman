*This project has been created as part of the 42 curriculum by gtourdia, kebertra*

# 42 Pac-Man, by sousampere &amp; keroberos68
A 42 project made by gtourdia &amp; kebertra, recreating the Pac-Man game in python.

# 📝​ Description

This project is a modern recreation of the iconic 1980s arcade classic, Pac-Man, developed in Python 3.10+.
The objective is to build a fully playable, modular game where players navigate a maze to consume all "pacgums" while avoiding four autonomous ghosts—Blinky, Pinky, Inky, and Clyde, each programmed with unique behaviors.

### Key technical highlights include:
- Dynamic Level Generation: Integration with an external "A-Maze-ing" package to generate unique maze structures for each level.
- Object-Oriented Architecture: A robust, reusable codebase featuring a polished graphical UI, a persistent highscore system, and a customizable game engine.
- Configuration & Customization: Deep game-state control through a JSON-based configuration system allowing for adjustable difficulty and level parameters.
- Professional Standards: Strict adherence to the flake8 coding standard, full type hinting with mypy, and comprehensive error handling to ensure a crash-free experience.

The final product is designed to be a deployment-ready package, suitable for distribution on public gaming platforms like Steam or Itch.io.

# 💻 Instructions

## Installation

```make install```

## Running

```make run ARGV=<configuration_path>```

or

```uv run python3 pac-man.py <configuration_path>```

# 🔧​​ Configuration

The provided configuration file must be a valid JSON file that supports comments with '#'.

Example :

```json
# This is an example of a configuration file format
{
  "highscore_filename": "data/leaderboard.json",
  "lives": 5,
  "pacgum_points": 15,
  "super_pacgum_points": 50,
  "ghost_points": 150,
  "seed": "forty-two",
  "max_time": 90,
  "level": [
    {
      "width": 10,
      "height": 10
    },
    {
      "width": 15,
      "height": 10
    }
  ]
}
```

# 🥇 Highscore

The highscore file path must be in the ./data folder, in a JSON format.

Depending on which error was triggered by your highscore file, the highscore file can be ignored by the program, or overridden if unreadable.

Example of a highscore file :

```json
[
    {
        "signature": "c0f3b6d07373aa4b239c2f1a99c9e6bb28b2f2d30cf1b1ba35123899056ed357",
        "scores": [
            {
                "username": "gambrinus",
                "score": 60
            }
        ]
    },
    {
        "signature": "f8e9a2242ba341419c7c446690210dceee74f9ae88b4675c63b8a11e4315fdd6",
        "scores": [
            {
                "username": "kebertra",
                "score": 1030
            },
            {
                "username": "gtourdia",
                "score": 42
            }
        ]
    }
]
```

In order to make highscores fair, scores are stored depending on the signature of the configuration file.

# 🌅​ Maze Generation

Maze generation is done in the MazeAdapter class that translates the generated maze from the provided MazeGenerator package into a usable maze for our implementation.

# 🔬​ Implementation

We used arcade for the game logic and graphical rendering.

Ghosts are using different algorithms (aggressive, semi-aggressive and random). The user should mostly be careful of the pink ghost.

Ghosts use a hitmap to calculate their path to the player (or the random spot)

Data is validated with precise error handling and pydantic validation.

# 🔗​ General Software Architecture

### Initialization

AssetValidator: Validate assets presence and format

ConfigParser: Parsing config

LeaderboardManager: Loading and exporting a leaderboard

### Entities

Ghost

Pacgum

Player

Super Pacgum

### Events

EventBus: Register and trigger events

### Managers

GameManager: Global session-level state handling (current_level, etc.)

CheatManager: Switching from normal to cheat mode

ScoreManager: Manages score (getting points, etc.)

SoundManager: Plays sounds in different conditions

### Rendering

Menu, pause, transition and finish views to render these different state

GameView using Renderer to render the game with the current GameState

### Maze

MazeAdapter to generate the maze with the given package

# 📖​ Resources

Since arcade has not a lot of community support or clear usage examples, we used AI for arcade related questions.

# 🚀 Project Management

Project Management is organized in different files in the project_management folder

This includes a GANTT diagram, requirement specifications, risks, team, technical architecture and a test plan.

[gtourdia / @sousampere](https://github.com/sousampere)

- Config and leaderboard loading and parsing
- Asset errors handling
- EventBus, SoundManager
- Visual rendering in different views
- Assets creation

[kebertra / @KeroBeros68](https://github.com/KeroBeros68)

- Initial project management
- Entities logic and interface (Entity, Movable, Ghost, Pacgum, Player, SuperPacgum)
- Ghost chase algorithms and hitmaps
- Code refactoring
- ScoreManager, CheatManager, GameManager

![Logo](https://github.com/sousampere/sousampere/blob/main/42mulhouse.png?raw=true)