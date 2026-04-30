# GANTT — Projet Pacman
*Kebertra + gtourdia — 10 semaines*

---

## Planning macro

```
S01 [░░░░░░░░░░░░] Conception & Setup
S02 [░░░░░░░░░░░░] Conception & Setup
S03 [░░░░░░░░░░░░] Core gameplay
S04 [░░░░░░░░░░░░] Core gameplay
S05 [░░░░░░░░░░░░] Core gameplay
S06 [░░░░░░░░░░░░] Fonctionnalités
S07 [░░░░░░░░░░░░] Fonctionnalités
S08 [░░░░░░░░░░░░] Qualité & Tests
S09 [░░░░░░░░░░░░] Packaging & Déploiement
S10 [░░░░░░░░░░░░] Soutenance
```

---

## Détail par semaine

### Phase 1 — Conception & Setup (S01–S02)

| Tâche | Assigné | S01 | S02 | Statut |
|---|---|---|---|---|
| Lecture complète du sujet | Kebertra + gtourdia | x | | |
| Redaction cahier des charges | Kebertra + gtourdia | x | | |
| Setup Git | Kebertra + gtourdia | x | | |
| Setup prévisionnel de l'architecture (classes, methodes, ...) | Kebertra + gtourdia | x | | |
| Makefile | gtourdia | x | | |
| Creation des classes Entity | Kebertra | | x | |
| Creation du ConfigLoader | Gtourdia | | x | |
| Creation du GameEngine (fenetre de base, events key press) | Gtourdia | | x | |
| Creation du MazeAdapter | Kebertra | | x | |

### Phase 2 — Core Gameplay (S03–S05)

| Tâche | Assigné | S03 | S04 | S05 | Statut |
|---|---|---|---|---|---|
| Rendu du labyrinthe (Arcade) | gtourdia | x |  | |  |
| Ajout joueur : déplacement/colisions | Kebertra | x |  | |  |
| Ajout pacgums (avec player interraction) | gtourdia | x | | | |
| Ajout super-pacgums | Kebertra | |  |  |  |
| Ajout ghost : mouvement autonome | gtourdia | |  |  |  |
| Ghost : mode edible + réapparition | gtourdia | | |  |  |
| Ecran game over | Kebertra | | |  |  |
| Boucle de jeu complète (GameEngine) | Kebertra + gtourdia | | |  |  |
| MVP jouable bout en bout | Kebertra + gtourdia | | |  |  |

### Phase 3 — Fonctionnalités (S06–S07)

| Tâche | Assigné | S06 | S07 | Statut |
|---|---|---|---|---|
| Highscore persistant | gtourdia |  |  | |  |
| Enchainement de niveaux 1 à 10+ | kebertra |  |  | |  |
| Menu principal (démarrer, highscores, instructions, quitter) | kebertra |  |  | |  |
| In-game HUD (score, vies, niveau, timer, progress) | gtourdia |  |  | |  |
| Menu pause + reprise | kebertra | | | |
| Game over screen + saisie nom | gtourdia | | | |
| Victory screen + saisie nom | gtourdia | | | |
| God Mode | kebertra | | | |

### Phase 4 — Qualité & Tests (S08)

| Tâche | Assigné | S08 | Statut |
|---|---|---|---|
| Conformité flake8 (PEP 8) | gtourdia |  |  |
| Typage complet + mypy sans erreur | Kebertra |  |  |
| Docstrings PEP 257 | Kebertra + gtourdia |  |  |
| Tests unitaires ConfigLoader | gtourdia |  |  |
| Tests unitaires ScoreManager | gtourdia |  |  |
| Tests unitaires MazeAdapter | Kebertra |  |  |
| Tests fonctionnels jeu complet | Kebertra + gtourdia |  |  |
| Revue croisée du code | Kebertra + gtourdia |  |  |

### Phase 5 — Packaging & Déploiement (S09)

| Tâche | Assigné | S09 | Statut |
|---|---|---|---|
| Script de packaging (PyInstaller) | Kebertra |  |  |
| Build Linux + test | gtourdia |  |  |
| Déploiement Steam ou Itch.io (build privé) | Kebertra + gtourdia |  |  |
| README complet en anglais | gtourdia |  |  |
| Vérification make lint final | Kebertra |  |  |

### Phase 6 — Soutenance (S10)

| Tâche | Assigné | S10 | Statut |
|---|---|---|---|
| Finalisation project_management/ | Kebertra + gtourdia |  |  |
| Revue de tout le code (prépa recode) | Kebertra + gtourdia |  |  |
| Vérification dépôt Git (noms de fichiers, structure) | gtourdia |  |  |
| Simulation peer review (cheat mode testé) | Kebertra |  |  |

---

## Suivi d'avancement

> Mettre à jour chaque semaine. Remplacer  par :white_check_mark: quand c'est terminé, par :warning: si en retard, par :x: si bloqué.

| Semaine | Prévu | Réalisé | Écart | Notes |
|---|---|---|---|---|
| S01 | Setup + CDC | | | |
| S02 | Archi + config | | | |
| S03 | Maze + rendu | | | |
| S04 | Player + entités | | | |
| S05 | MVP complet | | | |
| S06 | Score + menus | | | |
| S07 | Triche + niveaux | | | |
| S08 | Qualité + tests | | | |
| S09 | Build + déploiement | | | |
| S10 | Soutenance | | | |

---

*Dernière mise à jour : 29/04/2026*