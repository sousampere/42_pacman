# TEAM — Organisation de l'équipe
*Projet Pacman — Kebertra + gtourdia*

---

## Membres de l'équipe

| Login | Rôle principal | Forces identifiées |
|---|---|---|
| Kebertra | Référent architecture & rendu | Arcade, moteur de jeu, intégration A-Maze-ing |
| gtourdia | Référent qualité & features | Config, scoring, highscores, mode triche |

> Les rôles sont indicatifs. Les deux membres doivent comprendre et pouvoir expliquer l'intégralité du code lors de la peer review.

---

## Répartition des modules

| Module | Responsable principal | Relecteur |
|---|---|---|
| `pac-man.py` (point d'entrée) | gtourdia | Kebertra |
| `config.py` (ConfigLoader) | gtourdia | Kebertra |
| `maze.py` / `maze_adapter.py` | Kebertra | gtourdia |
| `game.py` (GameEngine) | Kebertra | gtourdia |
| `player.py` | gtourdia | Kebertra |
| `ghost.py` | Kebertra | gtourdia |
| `entities.py` (Pacgum, SuperPacgum) | gtourdia | Kebertra |
| `score.py` (ScoreManager) | gtourdia | Kebertra |
| `renderer.py` (Arcade) | Kebertra | gtourdia |
| `cheat.py` | gtourdia | Kebertra |
| Makefile | gtourdia | Kebertra |
| Tests unitaires | gtourdia | Kebertra |
| README.md | gtourdia | Kebertra |
| `project_management/` | Kebertra + gtourdia | — |

---

## Règles de collaboration

### Git
- Branche principale : `main` — toujours stable et fonctionnelle
- Développement sur des branches feature : `feature/<nom>` ou `fix/<nom>`
- Pas de push direct sur `main` — merge via Pull Request (ou accord verbal des deux membres)
- Commits en anglais, message clair : `feat: add ghost flee behavior` / `fix: config clamp on negative lives`

### Revue de code
- Tout nouveau module est relu par le coéquipier avant merge
- Objectif : les deux membres comprennent chaque ligne avant la soutenance
- Points de synchro : minimum 2 fois par semaine (à définir selon les agendas)

### Prise de décision
- Décisions techniques mineures : chacun décide sur son module
- Décisions techniques structurelles : accord des deux membres requis
- En cas de désaccord : on prototyper les deux options et on choisit la plus simple

---

## Journal des décisions techniques

> Ajouter une entrée à chaque décision importante. Cela servira lors de la soutenance pour justifier les choix.

| Date | Décision | Justification | Décidé par |
|---|---|---|---|
| 29/04/2026 | Bibliothèque graphique : Python Arcade | Moderne, bien documentée, adapté aux jeux 2D tile-based, cross-platform | Kebertra + gtourdia |
| 29/04/2026 | Highscores : JSON local | Simple, portable, requis par le sujet, pas de dépendance externe | Kebertra + gtourdia |
| 29/04/2026 | Packaging : PyInstaller | Standard Python, génère un exécutable standalone | Kebertra + gtourdia |
| À compléter | Comportement fin de timer | game over OU restart du niveau ? | |
| À compléter | Comportement fantômes : algo de chasse | BFS / distance Manhattan / aléatoire ? | |
| À compléter | Plateforme de déploiement | Steam ou Itch.io ? | |

---

## Points de blocage rencontrés

> Compléter au fil du projet. Utile pour la section "Summary of blocking points" demandée par le sujet.

| Date | Blocage | Solution apportée | Durée perdue |
|---|---|---|---|
| À compléter | | | |

---

*Dernière mise à jour : 29/04/2026*