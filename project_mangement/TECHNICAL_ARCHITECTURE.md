
# Technical architecture : functions, classes and methods

## pac-man.py

```
main():
- Load config avec ConfigLoader()
- Cree le GameEngine depuis la config
```

## src/ConfigLoader.py

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

## src/MazeAdapter.py

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

## src/GameEngine.py

```
GameEngine:
- render_menu()
  > Affiche le menu
- render_game()
  > Affiche un niveau
- render_pause()
  > Affiche un menu de pause
- render_finish()
  > Affiche un menu de partie terminee

- Listen to keys / even
```
