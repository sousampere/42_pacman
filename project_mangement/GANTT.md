# GANTT — Projet Pacman
*Kebertra + Gtourdiat — 10 semaines*

---

## Planning macro

```
S01 [████████░░░░░░░░░░░░] Conception & Setup
S02 [████████░░░░░░░░░░░░] Conception & Setup
S03 [░░░░████████░░░░░░░░] Core gameplay
S04 [░░░░████████░░░░░░░░] Core gameplay
S05 [░░░░████████░░░░░░░░] Core gameplay
S06 [░░░░░░░░████████░░░░] Fonctionnalités
S07 [░░░░░░░░████████░░░░] Fonctionnalités
S08 [░░░░░░░░░░░░████████] Qualité & Tests
S09 [░░░░░░░░░░░░████████] Packaging & Déploiement
S10 [░░░░░░░░░░░░████████] Soutenance
```

---

## Détail par semaine

### Phase 1 — Conception & Setup (S01–S02)

| Tâche | Assigné | S01 | S02 | Statut |
|---|---|---|---|---|
| Lecture complète du sujet | Kebertra + Gtourdiat | ██ | | ☐ |
| Rédaction du cahier des charges | Kebertra + Gtourdiat | ██ | | ☐ |
| Setup dépôt Git + structure projet | Kebertra | ██ | | ☐ |
| Makefile (install, run, debug, clean, lint) | Gtourdiat | ██ | | ☐ |
| Prise en main du package A-Maze-ing | Kebertra + Gtourdiat | | ██ | ☐ |
| Prise en main de Python Arcade | Kebertra | | ██ | ☐ |
| Définition de l'architecture modulaire | Kebertra + Gtourdiat | | ██ | ☐ |
| ConfigLoader (JSON + commentaires #) | Gtourdiat | | ██ | ☐ |

### Phase 2 — Core Gameplay (S03–S05)

| Tâche | Assigné | S03 | S04 | S05 | Statut |
|---|---|---|---|---|---|
| MazeAdapter (intégration A-Maze-ing) | Kebertra | ██ | | | ☐ |
| Rendu du labyrinthe (Arcade) | Kebertra | ██ | ██ | | ☐ |
| Player : déplacement, collisions murs | Gtourdiat | ██ | ██ | | ☐ |
| Entités : Pacgum, SuperPacgum | Gtourdiat | | ██ | | ☐ |
| Ghost : mouvement autonome | Kebertra | | ██ | ██ | ☐ |
| Ghost : mode edible + réapparition | Kebertra | | | ██ | ☐ |
| Système de vies + game over | Gtourdiat | | | ██ | ☐ |
| Boucle de jeu complète (GameEngine) | Kebertra + Gtourdiat | | | ██ | ☐ |
| MVP jouable bout en bout | Kebertra + Gtourdiat | | | ██ | ☐ |

### Phase 3 — Fonctionnalités (S06–S07)

| Tâche | Assigné | S06 | S07 | Statut |
|---|---|---|---|---|
| Système de score | Gtourdiat | ██ | | ☐ |
| Highscores persistants (JSON, top 10) | Gtourdiat | ██ | ██ | ☐ |
| Menu principal (démarrer, highscores, instructions, quitter) | Kebertra | ██ | | ☐ |
| HUD in-game (score, vies, niveau, timer) | Kebertra | ██ | | ☐ |
| Menu pause + reprise | Gtourdiat | | ██ | ☐ |
| Écran Game Over + saisie nom | Kebertra | | ██ | ☐ |
| Écran Victoire | Kebertra | | ██ | ☐ |
| Mode triche complet (5 fonctions) | Gtourdiat | ██ | ██ | ☐ |
| Progression 10 niveaux | Kebertra + Gtourdiat | | ██ | ☐ |

### Phase 4 — Qualité & Tests (S08)

| Tâche | Assigné | S08 | Statut |
|---|---|---|---|
| Conformité flake8 (PEP 8) | Gtourdiat | ██ | ☐ |
| Typage complet + mypy sans erreur | Kebertra | ██ | ☐ |
| Docstrings PEP 257 | Kebertra + Gtourdiat | ██ | ☐ |
| Tests unitaires ConfigLoader | Gtourdiat | ██ | ☐ |
| Tests unitaires ScoreManager | Gtourdiat | ██ | ☐ |
| Tests unitaires MazeAdapter | Kebertra | ██ | ☐ |
| Tests fonctionnels jeu complet | Kebertra + Gtourdiat | ██ | ☐ |
| Revue croisée du code | Kebertra + Gtourdiat | ██ | ☐ |

### Phase 5 — Packaging & Déploiement (S09)

| Tâche | Assigné | S09 | Statut |
|---|---|---|---|
| Script de packaging (PyInstaller) | Kebertra | ██ | ☐ |
| Build Linux + test | Gtourdiat | ██ | ☐ |
| Déploiement Steam ou Itch.io (build privé) | Kebertra + Gtourdiat | ██ | ☐ |
| README complet en anglais | Gtourdiat | ██ | ☐ |
| Vérification make lint final | Kebertra | ██ | ☐ |

### Phase 6 — Soutenance (S10)

| Tâche | Assigné | S10 | Statut |
|---|---|---|---|
| Finalisation project_management/ | Kebertra + Gtourdiat | ██ | ☐ |
| Revue de tout le code (prépa recode) | Kebertra + Gtourdiat | ██ | ☐ |
| Vérification dépôt Git (noms de fichiers, structure) | Gtourdiat | ██ | ☐ |
| Simulation peer review (cheat mode testé) | Kebertra | ██ | ☐ |

---

## Suivi d'avancement

> Mettre à jour chaque semaine. Remplacer ☐ par :white_check_mark: quand c'est terminé, par :warning: si en retard, par :x: si bloqué.

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