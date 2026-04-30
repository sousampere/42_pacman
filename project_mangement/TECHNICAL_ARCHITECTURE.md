
# Technical architecture : functions, classes and methods

## pac-man.py

```
main():
- Load arguments avec argparse
- Load config avec ConfigLoader()
- Cree le GameEngine depuis la config
```

## src/arguments.py

```
Les arguments sont set avec argparse

Arguments:
--config (ou 1er arg si pas de flag): str | chemin vers le fichier de config
--theme: str | chemin vers le dossier de theme
```

## src/config_loader.py

```
Config(BaseModel):
- highscore_filename: str | Fichier output des scores
- level: ?
- lvl_width: int | Largeur du niveau
- lvl_height: int | Longueur du niveau
- lives: int | Nombre de vies
- nb_pacgum: int | Nombre de pacgums
- pacgum_points: int | Points par pacgums
- super_pacgum_points: int | Points par super-pacgums
- ghost_points: int | Point par fantome
- seed: str | Seed du premier niveau
- max_time: int | Temps (en secondes) maximum pour realiser le niveau

AbsConfigLoader(ABC):
- load_config(source: str) -> Config
  > Methode abstraite pour obtenir une config a partir d'une source

ConfigLoader(AbsConfigLoader):
- load_config(source: str) -> Config
  > Ouvre un fichier source et le transforme en objet Config
```

## src/maze_adapter.py

```
Cell:
- __hex_value: str | hexadecimal value of the cell
- __x: int | x coord
- __y: int | y coord

Maze:
- list[list[Cell]] | Tableau 2D de cellules composant le labyrinthe

AbsMazeAdapter(ABC):
- create_maze(width: int, height: int, seed: str | None) -> Maze
  > abstractmethod to get a Maze object

MazeAdapter(AbsMazeAdapter):
- create_maze(width: int, height: int, seed: str | None) -> Maze
  > Use the A-Maze-Ing package to get a maze with the given data, output a Maze object
```

## src/entities.py

```
(À compléter par kebertra)
```

## src/game_views.py

```
MenuView(arcade.View):
  > ...

GameView(arcade.View):
  > ...

# Note: Le on_draw() du PauseView appelle le on_draw du GameView pour faire une superposition
PauseView(arcade.View):
  > ...

FinishView(arcade.View):
```

## src/game_engine.py

```
GameEngine(arcade.Window):
- maze_adapter: MazeAdapter | Pour générer des maze
- config: Config | Pour accéder à la config
- menu_view: arcade.View | Scene de menu
- game_view: arcade.View | Scene in-game
- pause_view: arcade.View | Scene de pause
- finish_view: arcade.View | Scene de finish

- render_menu()
  > Affiche le menu
- render_game()
  > Affiche un niveau
- render_pause()
  > Affiche un menu de pause
- render_finish()
  > Affiche un menu de partie terminee
- save_score(nickname: str, score: int, time: int, config_hash: str) -> None
  > Enregistre dans le leaderboard la score
- (diverses fonctions surchargées pour gérer les events)
```
