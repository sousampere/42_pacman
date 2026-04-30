# CAHIER DES CHARGES
## Projet Pacman — Ghosts! More ghosts!
*Sujet 42 — Version 1.2*

---

| Champ | Valeur |
|---|---|
| Version | 1.0 |
| Date | 29/04/2026 |
| Auteur(s) | Kebertra — gtourdia |
| Statut | Brouillon |
| Langage | Python 3.10+ |
| Bibliothèque graphique | Arcade (Python) |
| Plateforme cible | Steam ou Itch.io (à décider — build privé/unlisted) |
| OS de développement | Linux |

---

## Sommaire

1. [Présentation du projet](#1-présentation-du-projet)
2. [Périmètre fonctionnel](#2-périmètre-fonctionnel)
3. [Exigences techniques](#3-exigences-techniques)
4. [Architecture et intégrations](#4-architecture-et-intégrations)
5. [Spécifications du jeu](#5-spécifications-du-jeu)
6. [Interface utilisateur](#6-interface-utilisateur)
7. [Livrables et planning](#7-livrables-et-planning)
8. [Contraintes et hypothèses](#8-contraintes-et-hypothèses)
9. [Critères de recette](#9-critères-de-recette)
10. [Annexes](#10-annexes)

---

## 1. Présentation du projet

### 1.1 Contexte

Ce projet s'inscrit dans le cursus 42 et consiste à recréer le jeu d'arcade Pac-Man (Namco, 1980) en Python moderne, avec une architecture orientée-objet, un pipeline de qualité de code (flake8 + mypy) et un déploiement sur une plateforme de jeux publique.

Le jeu doit intégrer un générateur de labyrinthes externe (package A-Maze-ing fourni par un autre groupe), un système de highscores persistant et un mode triche dédié à la revue par les pairs.

### 1.2 Objectifs

- Produire un jeu Pac-Man complet, jouable et déployable.
- Respecter les standards de qualité 42 : flake8, mypy, docstrings PEP 257, gestion d'exceptions.
- Intégrer un générateur de labyrinthe externe sans le modifier.
- Mettre en place un système de highscores persistant (JSON).
- Fournir un mode triche opérationnel pour l'évaluation.
- Livrer une documentation complète (README, cahier des charges, suivi de projet).

### 1.3 Vision

> Permettre à un joueur de vivre une expérience Pac-Man fidèle à l'original, sur 10+ niveaux générés procéduralement, depuis une interface graphique soignée, téléchargeable librement sur une plateforme publique.

### 1.4 Parties prenantes

| Rôle | Nom / Login | Responsabilité |
|---|---|---|
| Commanditaire | École 42 | Définition du sujet, évaluation |
| Chef de projet | Kebertra / gtourdia | Coordination, gestion du dépôt Git |
| Développeurs | Kebertra + gtourdia | Réalisation, tests |
| Évaluateurs (pairs) | Autres étudiants 42 | Revue par les pairs, cheat mode |

---

## 2. Périmètre fonctionnel

### 2.1 Fonctionnalités — MoSCoW

**Must have (indispensable)**

- [❌] Lancement via `python3 pac-man.py config.json`
- [❌] Lecture et validation du fichier de configuration JSON (avec commentaires `#`) avec :
    - [❌] Chemin de highscore
    - [❌] Liste des niveaux
        - [❌] width
        - [❌] height
        - [❌] seed
        - [❌] level_max_time
    - [❌] Nombre de vies
    - [❌] Nombre de pacgums
    - [❌] Points par pacgums
    - [❌] Points par super-pacgums
    - [❌] Points par fantôme
    - [❌] Seed
    - [❌] Temps max par level
- [❌] Gestion robuste des erreurs de config (clamping, pas de traceback)
- [❌] Génération des labyrinthes via le package A-Maze-ing assigné (`PERFECT=False`)
- [❌] Déplacement du joueur (4 directions, corridors uniquement)
- [❌] 4 fantômes autonomes avec comportements distincts
- [❌] Pacgums et Super-pacgums (power pellets dans les 4 coins)
- [❌] Système de vies (3 vies par défaut, game over à 0)
- [❌] Système de score (pacgum +10, super-pacgum +50, fantôme mangé +200)
- [❌] 10 niveaux minimum avec limite de temps (90s par défaut)
- [❌] Système de highscores persistant (JSON, top 10)
- [❌] Interface graphique complète (menu, HUD, pause, game over, victoire)
    - [❌] Menu avec leaderboard
    - [❌] HUD
    - [❌] Pause
    - [❌] Game over / Victory
- [❌] Mode triche
    - [❌] Invincibilité
    - [❌] Level skip
    - [❌] Freeze fantômes
    - [❌] Vies bonus
    - [❌] Speed hack
- [❌] Déploiement sur Steam ou Itch.io (build privé/unlisted)
- [❌] Makefile avec cibles : `install`, `run`, `debug`, `clean`, `lint`
    - [❌] Rule install
    - [❌] Rule run
    - [❌] Rule debug
    - [❌] Rule clean
    - [❌] Rule lint
- [❌] README complet en anglais

**Should have (important)**

- [❌] IA fantômes différenciée (chase, ambush, aléatoire, erratique)
- [❌] Animations
    - [❌] Pac-man ouvre et ferme la bouche
    - [❌] Fantômes clignotants
    - [❌] Animation de "mort"
- [❌] Sons / effets audio
- [❌] Fichier `.gitignore`
- [❌] Tests unitaires (pytest ou unittest)

**Could have (souhaitable)**

- [❌] Skins / thèmes visuels alternatifs
- [❌] Tableau des highscores animé
- [❌] Support manette de jeu

**Won't have (hors périmètre)**

- [❌] Mode multijoueur (leaderboard)
- [❌] Éditeur de niveaux
- [❌] Générateur de labyrinthe maison (interdit par le sujet)

### 2.2 User Stories

| ID | Rôle | Action souhaitée | Bénéfice | Priorité |
|---|---|---|---|---|
| US-01 | Joueur | Lancer le jeu avec un fichier de config | Personnaliser la partie | Must |
| US-02 | Joueur | Déplacer Pac-Man dans le labyrinthe | Jouer au jeu | Must |
| US-03 | Joueur | Manger des pacgums et fantômes | Augmenter son score | Must |
| US-04 | Joueur | Voir son score et ses vies en temps réel | Suivre sa progression | Must |
| US-05 | Joueur | Entrer son nom en fin de partie | Sauvegarder son highscore | Must |
| US-06 | Joueur | Mettre la partie en pause | Gérer les interruptions | Must |
| US-07 | Évaluateur | Activer le mode triche | Tester toutes les fonctionnalités | Must |
| US-08 | Joueur | Progresser sur 10+ niveaux | Avoir un challenge croissant | Must |
| US-09 | Joueur | Voir les highscores dans le menu | Comparer avec les autres | Should |

---

## 3. Exigences techniques

### 3.1 Stack technologique

| Composant | Technologie | Justification |
|---|---|---|
| Langage | Python 3.10+ | Requis par le sujet 42 |
| Graphisme | Python Arcade 2.x | Bibliothèque moderne, bien documentée, cross-platform, adaptée aux jeux 2D tile-based |
| Configuration | JSON (avec commentaires `#`) | Requis par le sujet |
| Persistance scores | JSON sur disque | Simple, portable, requis sujet |
| Génération labyrinthe | Package A-Maze-ing (externe) | Assigné par l'école, `PERFECT=False` |
| Qualité code | flake8 + mypy | Requis par le sujet |
| Tests | pytest | Recommandé par le sujet |
| Packaging | PyInstaller ou équivalent | Déploiement Steam/Itch.io |
| Déploiement | Steam ou Itch.io (à décider) | Requis par le sujet — build privé/unlisted |
| Gestionnaire deps | uv | Via `make install` |

### 3.2 Performances

| Critère | Valeur cible |
|---|---|
| FPS cible | 60 FPS stables |
| Temps de chargement d'un niveau | < 2 secondes |
| Temps de réponse aux entrées clavier | < 50 ms |
| Taille du build packagé | < 200 Mo |

### 3.3 Qualité et conformité

- [❌] Conformité flake8 (PEP 8)
- [❌] Typage complet — mypy sans erreur (`--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`)
- [❌] Docstrings PEP 257 sur toutes les fonctions et classes
- [❌] Gestion des exceptions (try/except, context managers, jamais de traceback exposé)
- [❌] Fichier `.gitignore` incluant `__pycache__`, `.mypy_cache`, `venv`

### 3.4 Compatibilité

| Type | Cible |
|---|---|
| OS développement | Linux (Ubuntu / Debian) |
| OS cible (build packagé) | Linux, macOS, Windows (via PyInstaller) |
| Python | 3.10 ou supérieur |
| Résolution minimale | 800x600 (recommandé 1280x720) |
| Clavier | AZERTY et QWERTY (flèches directionnelles ou WASD/ZQSD) |

---

## 4. Architecture et intégrations
 
L'architecture retenue est un **hybride à trois couches** : hiérarchie d'entités avec abstraction, State Machine sur le `GameEngine`, et `EventBus` léger pour découpler les managers transversaux.
 
### 4.1 Schéma d'architecture haut niveau
 
```
pac-man.py  →  ConfigLoader  →  GameEngine
                                    │
                                    ├── StateMachine
                                    │       ├── MenuState
                                    │       ├── PlayingState  ──── list[Entity]
                                    │       │                         ├── Player      (Entity+Movable)
                                    │       │                         ├── Ghost × 4   (Entity+Movable)
                                    │       │                         ├── Pacgum × N  (Entity+Collectible)
                                    │       │                         └── SuperPacgum×4 (Entity+Collectible)
                                    │       ├── PausedState
                                    │       └── GameOverState
                                    │
                                    ├── EventBus  ←── publish(event)
                                    │       ├── ScoreManager  →  highscores.json
                                    │       ├── LivesManager
                                    │       └── SoundManager  (optionnel)
                                    │
                                    ├── MazeAdapter  →  [A-Maze-ing pkg]
                                    ├── Renderer     →  [Python Arcade]
                                    └── CheatManager
```


 
### 4.2 Les trois couches de l'architecture hybride
 
#### Couche 1 — Hiérarchie d'entités (Entity / Movable / Collectible)
 
Toutes les entités partagent une classe abstraite `Entity` et implémentent les interfaces correspondant à leurs capacités. Le `PlayingState` manipule uniquement des `list[Entity]` sans connaître les types concrets.
 
```
Entity (abstract)          position, size, update(dt), draw()
│
├── + Movable (interface)  move(), get_speed()
│       ├── Player         handle_input(), die(), respawn()
│       └── Ghost          chase(), flee(), is_edible, home_corner
│
└── + Collectible (interface)  collect(), get_points()
        ├── Pacgum             points = 10
        └── SuperPacgum        points = 50, activate_power()
```
 
#### Couche 2 — State Machine (sur GameEngine)
 
Le `GameEngine` délègue entièrement `update(dt)` et `draw()` à l'état courant. Chaque `State` implémente `on_enter()`, `on_exit()`, `update(dt)`, `draw()`.
 
```
State (abstract)
├── MenuState       affiche menu + highscores
├── PlayingState    boucle de jeu, gère list[Entity] + EventBus
├── PausedState     overlay pause, jeu suspendu
└── GameOverState   score final, saisie nom, sauvegarde highscore
```
 
Transitions déclenchées par événements :
- `MenuState` → `PlayingState` : action "start"
- `PlayingState` → `PausedState` : touche pause
- `PausedState` → `PlayingState` : reprise
- `PlayingState` → `GameOverState` : `PLAYER_DIED` (0 vies) ou `LEVEL_TIME_UP`
- `GameOverState` → `MenuState` : retour menu
#### Couche 3 — EventBus (découplage des managers)
 
Le `PlayingState` publie des événements sur l'`EventBus`. Les managers s'y abonnent à l'initialisation et réagissent sans être couplés aux entités.
 
| Événement publié | Abonnés | Action déclenchée |
|---|---|---|
| `PACGUM_EATEN(pts)` | `ScoreManager`, `SoundManager` | +score, son waka |
| `SUPER_PACGUM_EATEN(pts)` | `ScoreManager`, `SoundManager` | +score, ghosts edibles, son power |
| `GHOST_EATEN(pts)` | `ScoreManager`, `SoundManager` | +score, son ghost |
| `PLAYER_DIED` | `LivesManager`, `SoundManager` | -1 vie, son death |
| `LEVEL_COMPLETE` | `ScoreManager`, `GameEngine` | transition niveau suivant |
| `LEVEL_TIME_UP` | `GameEngine` | transition game over |
| `GHOST_EDIBLE_END` | `SoundManager` | fin du mode power |
 
> **Pourquoi pas full Event-Driven ?** Les entités (`Player`, `Ghost`…) communiquent toujours directement via leurs méthodes dans `PlayingState` — seuls les managers transversaux (score, vies, son) passent par l'`EventBus`. Cela évite un flux illisible tout en découplant ce qui doit l'être.
 
#### Modules
 
| Module | Contenu | Dépendances |
|---|---|---|
| `pac-man.py` | Point d'entrée, parsing args | `config.py`, `game.py` |
| `config.py` | `ConfigLoader` — JSON + commentaires `#`, clamping | stdlib `json`, `logging` |
| `game.py` | `GameEngine` + `StateMachine` — boucle Arcade, transitions | `state.py`, tous |
| `state.py` | `State` (abstract), `MenuState`, `PlayingState`, `PausedState`, `GameOverState` | `entity.py`, `event.py` |
| `event.py` | `EventBus` — publish/subscribe, typage des événements | stdlib `abc` |
| `entity.py` | `Entity` (abstract), interfaces `Movable` et `Collectible` | stdlib `abc` |
| `player.py` | `Player(Entity, Movable)` — input, die(), respawn() | `entity.py`, `maze_adapter.py` |
| `ghost.py` | `Ghost(Entity, Movable)` — IA chase/flee, edible, respawn() | `entity.py`, `maze_adapter.py` |
| `pacgum.py` | `Pacgum(Entity, Collectible)` — points=10 | `entity.py` |
| `super_pacgum.py` | `SuperPacgum(Entity, Collectible)` — points=50, activate_power() | `entity.py` |
| `maze_adapter.py` | Adaptateur A-Maze-ing (`PERFECT=False`), fallback si erreur | A-Maze-ing pkg |
| `score.py` | `ScoreManager` — score courant, highscores JSON top 10 | stdlib `json`, `event.py` |
| `lives.py` | `LivesManager` — compteur vies, abonné `PLAYER_DIED` | `event.py` |
| `renderer.py` | Rendu Arcade, HUD, animations | Python Arcade |
| `cheat.py` | `CheatManager` — invincibilité, level skip, freeze, vies, vitesse | `game.py`, `event.py` |
 
### 4.3 Modèle de données

**Configuration (`config.json`)**

- `highscore_filename` : str
- `levels` : liste de niveaux (`width`, `height`, `seed`, `level_max_time`)
- `lives` : int (défaut 3)
- `pacgum` : int (défaut 42 — nombre de pacgums)
- `points_per_pacgum` : int (défaut 10)
- `points_per_super_pacgum` : int (défaut 50)
- `points_per_ghost` : int (défaut 200)
- `seed` : int (défaut 42, niveau 1 fixé)
- `level_max_time` : int (défaut 90 secondes)

**Highscores (`highscores.json`)**

- Liste de 10 entrées max : `{ "name": str (10 car., alphanum + espaces), "score": int >= 0 }`
- Triée par score décroissant
- Chargée au démarrage, sauvegardée en fin de partie

---

## 5. Spécifications du jeu

### 5.1 Structure d'un niveau

- Labyrinthe généré par le package A-Maze-ing assigné (`PERFECT=False`)
- Niveau 1 : seed fixe (42) — niveaux suivants : seed aléatoire
- Pacgums (petits points) dans la majorité des couloirs
- Super-pacgums (gros points) dans les 4 coins du labyrinthe
- 4 fantômes positionnés un dans chaque coin
- Le joueur démarre au centre du labyrinthe

### 5.2 Joueur

- Déplacement dans 4 directions (flèches ou WASD/ZQSD), corridors uniquement
- 3 vies au départ (configurable)
- Perd une vie au contact d'un fantôme (non-edible)
- Réapparaît au centre après avoir perdu une vie
- Game over quand toutes les vies sont perdues
- Victoire de niveau quand tous les pacgums sont mangés
- Victoire globale quand tous les niveaux sont terminés
- Le score et les vies restantes sont conservés entre les niveaux

### 5.3 Fantômes

- 4 fantômes, mouvement autonome dans les corridors
- Mode normal : pourchassent le joueur (comportement libre : distance, BFS, aléatoire…)
- Mode edible : fuient le joueur pendant un temps limité après un super-pacgum
- Après avoir été mangé : réapparaît dans son coin après 5 à 10 secondes

### 5.4 Scoring

| Action | Points |
|---|---|
| Manger un pacgum | +10 pts (configurable) |
| Manger un super-pacgum | +50 pts (configurable) |
| Manger un fantôme edible | +200 pts (configurable) |
| Le score ne diminue jamais | — |

### 5.5 Progression

- 10 niveaux minimum
- Limite de temps par niveau (défaut 90s) — comportement en fin de temps : à définir (game over ou restart)
- Pause / reprise disponible pendant la partie

### 5.6 Mode triche

| Fonctionnalité | Description |
|---|---|
| Invincibilité | Les fantômes ne peuvent pas manger le joueur |
| Level skip | Passer immédiatement au niveau suivant |
| Freeze fantômes | Les fantômes s'arrêtent de bouger |
| Vies bonus | Ajouter des vies supplémentaires |
| Vitesse augmentée | Le joueur se déplace plus vite |

---

## 6. Interface utilisateur

| Écran | Éléments |
|---|---|
| Menu principal | Démarrer, Highscores (top 10), Instructions, Quitter |
| HUD in-game | Score courant, Vies restantes, Niveau actuel, Temps restant |
| Menu pause | Reprendre, Retour menu principal |
| Game Over | Score final, saisie nom joueur (sauvegarde highscore) |
| Victoire | Score final + message félicitations, saisie nom joueur |

---

## 7. Livrables et planning

### 7.1 Livrables

| Livrable | Description | Format | Date cible |
|---|---|---|---|
| Cahier des charges | Ce document | MD / DOCX | Dès démarrage |
| Dépôt Git | Code source complet + Makefile + packaging script | Git | Continu |
| README.md | Documentation complète en anglais | Markdown | Avant soutenance |
| `project_management/` | Timeline, suivi avancement, analyse risques, orga équipe | Markdown / PDF | Continu |
| Build packagé | Jeu fonctionnel sur Steam ou Itch.io | Build privé | Avant soutenance |
| MVP (fonctionnalités Must) | Jeu jouable de bout en bout | Déployé | Fin S5 (~mi-parcours) |

### 7.2 Planning macro (~10 semaines)

| Phase | Contenu | Durée estimée |
|---|---|---|
| Phase 1 — Conception (S1-S2) | Architecture, CDC, choix techniques, prise en main A-Maze-ing + Arcade | 2 semaines |
| Phase 2 — Core gameplay (S3-S5) | Moteur de jeu, joueur, fantômes, labyrinthes, collisions | 3 semaines |
| Phase 3 — Fonctionnalités (S6-S7) | Highscores, mode triche, menus complets, HUD | 2 semaines |
| Phase 4 — Qualité (S8) | Lint flake8/mypy, tests, gestion d'erreurs exhaustive | 1 semaine |
| Phase 5 — Packaging (S9) | Build PyInstaller, déploiement plateforme, README | 1 semaine |
| Phase 6 — Soutenance (S10) | Documentation projet, revue finale, préparation recode | 1 semaine |

---

## 8. Contraintes et hypothèses

### 8.1 Contraintes

| Type | Description |
|---|---|
| Technique — langage | Python 3.10+ obligatoire |
| Technique — linting | flake8 et mypy sans erreur (flags obligatoires du sujet) |
| Technique — externe | Utiliser le package A-Maze-ing assigné as-is (ne pas le modifier) |
| Technique — config | Le fichier de config sera modifié pendant la soutenance |
| Ressources | Équipe de 2 développeurs (Kebertra + gtourdia) |
| Organisationnelle | Soumission via dépôt Git uniquement |
| Légale | Build déployé en privé/unlisted sur la plateforme choisie |
| Pédagogique | Tout code généré par IA doit être compris et explicable par l'équipe |

### 8.2 Hypothèses

- Le package A-Maze-ing assigné expose bien un paramètre `PERFECT` et une interface documentée.
- La bibliothèque Python Arcade est compatible avec l'environnement Linux de développement.
- Le build packagé peut être généré et re-généré pendant la soutenance.
- Les évaluateurs disposent d'un clavier standard (flèches directionnelles disponibles).

---

## 9. Critères de recette

### 9.1 Processus de validation

1. Revue fonctionnelle par les pairs (peer review 42)
2. Tests manuels de tous les cas d'usage (cheat mode inclus)
3. Vérification lint : `make lint` sans erreur
4. Vérification déploiement : jeu téléchargeable et fonctionnel depuis la plateforme
5. Possible recode à la demande de l'évaluateur

### 9.2 Critères d'acceptation

| Fonctionnalité | Critère de succès |
|---|---|
| Lancement | `python3 pac-man.py config.json` démarre sans traceback |
| Config invalide | Message d'erreur clair, clamping sur défauts, pas de crash |
| Labyrinthe | Généré par le package assigné, `PERFECT=False`, corridors Pac-Man compatibles |
| Déplacement joueur | Fluide, limité aux corridors, 4 directions |
| Fantômes | 4 fantômes autonomes, mode edible, réapparition au coin |
| Scoring | Scores corrects pour pacgum / super-pacgum / fantôme mangé |
| Highscores | Sauvegardés et chargés correctement, top 10, entrée nom joueur |
| Mode triche | Toutes les fonctions activables et fonctionnelles |
| Qualité code | `make lint` passe sans erreur (flake8 + mypy) |
| Déploiement | Jeu installable et jouable depuis Steam ou Itch.io |

### 9.3 Tests attendus

- [❌] Tests unitaires ConfigLoader (valeurs invalides, clés manquantes, commentaires `#`)
- [❌] Tests unitaires ScoreManager (ajout score, tri, persistance, nom invalide)
- [❌] Tests unitaires MazeAdapter (échec générateur, dimensions invalides)
- [❌] Tests fonctionnels jeu complet (win, lose, pause, cheat mode)
- [❌] Test de charge : 10 niveaux enchaînés sans fuite mémoire

---

## 10. Annexes

### 10.1 Glossaire

| Terme | Définition |
|---|---|
| Pacgum | Petit point collectible dans les couloirs — +10 pts |
| Super-pacgum | Grand point dans les coins, rend les fantômes edibles — +50 pts |
| Edible | État d'un fantôme après qu'un super-pacgum a été mangé (peut être dévoré) |
| A-Maze-ing | Package externe de génération de labyrinthes assigné par l'école |
| `PERFECT=False` | Paramètre A-Maze-ing générant des labyrinthes avec boucles (compatibles Pac-Man) |
| Cheat mode | Mode de débogage facilitant la revue par les pairs |
| HUD | Heads-Up Display — interface superposée pendant le jeu (score, vies, timer) |
| MoSCoW | Must / Should / Could / Won't — méthode de priorisation |
| flake8 | Linter Python (conformité PEP 8) |
| mypy | Vérificateur de types statique Python |

### 10.2 Documents de référence

- Sujet 42 : Pacman — Ghosts! More ghosts! v1.2
- Template cahier des charges fourni
- Documentation du package A-Maze-ing assigné
- Documentation Arcade : https://api.arcade.academy/
- PEP 257 — Docstring Conventions
- OWASP Python Security Guidelines

### 10.3 Historique des révisions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 1.0 | 29/04/2026 | Kebertra / gtourdia | Création initiale |
