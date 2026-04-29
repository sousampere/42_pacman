# RISKS — Analyse des risques
*Projet Pacman — Kebertra + Gtourdiat*

---

## Matrice des risques

| ID | Risque | Probabilité | Impact | Criticité |
|---|---|---|---|---|
| R01 | Interface du package A-Maze-ing incompatible ou mal documentée | Moyenne | Élevé | :red_circle: Critique |
| R02 | Config modifiée pendant la soutenance → crash ou comportement inattendu | Élevée | Élevé | :red_circle: Critique |
| R03 | mypy ou flake8 échoue en dernière minute (typage incomplet) | Moyenne | Élevé | :red_circle: Critique |
| R04 | Build PyInstaller ne fonctionne pas sur la plateforme cible | Moyenne | Élevé | :red_circle: Critique |
| R05 | Retard sur le Core gameplay → MVP pas prêt à mi-parcours | Moyenne | Moyen | :large_orange_circle: Élevé |
| R06 | Arcade incompatible avec l'environnement Linux de l'évaluateur | Faible | Élevé | :large_orange_circle: Élevé |
| R07 | Mode triche incomplet → points perdus à la peer review | Faible | Moyen | :large_yellow_circle: Modéré |
| R08 | Mauvaise gestion des erreurs → traceback visible pendant la soutenance | Faible | Élevé | :large_orange_circle: Élevé |
| R09 | Un membre de l'équipe indisponible sur une période clé | Faible | Moyen | :large_yellow_circle: Modéré |
| R10 | Highscores corrompus ou perdus (fichier JSON invalide) | Faible | Faible | :large_green_circle: Faible |

---

## Détail et mitigation

### :red_circle: R01 — Package A-Maze-ing incompatible ou mal documentée

**Description** : Le package est produit par un autre groupe d'étudiants. Son interface peut être instable, mal documentée, ou changer entre le moment où on le reçoit et la peer review (le sujet précise qu'il sera réinstallé lors de la revue).

**Mitigation** :
- Lire la documentation du package dès S01, tester toutes les fonctions exposées.
- Écrire `maze_adapter.py` comme une couche d'abstraction complète : si l'interface change, seul l'adaptateur est à modifier.
- Prévoir un fallback : si le générateur lève une exception, afficher un message clair et proposer un labyrinthe de secours codé en dur (pour ne pas bloquer la démo).
- Ne jamais modifier le package (interdit par le sujet).

**Indicateur d'alerte** : L'adaptateur plante lors du premier test en S02.

---

### :red_circle: R02 — Config modifiée pendant la soutenance

**Description** : Le sujet indique explicitement que la configuration sera modifiée lors de la défense. Des valeurs invalides, manquantes, ou hors limites seront probablement injectées.

**Mitigation** :
- Implémenter un clamping systématique sur toutes les valeurs (min/max définis et documentés dans le README).
- Tester avec des configs volontairement cassées dès S04 (clé manquante, valeur négative, type incorrect, fichier vide, fichier absent).
- Jamais de traceback exposé : tous les chemins d'erreur retournent un message clair et continuent avec les défauts.
- Documenter chaque clé et sa valeur par défaut dans le README.

**Indicateur d'alerte** : Un `KeyError` ou `ValueError` non intercepté lors des tests de S04.

---

### :red_circle: R03 — mypy / flake8 échoue en dernière minute

**Description** : Ignorer le typage et le linting pendant le développement pour aller vite, puis découvrir des dizaines d'erreurs en S08.

**Mitigation** :
- Intégrer `make lint` dans la routine de développement dès S01 — le lancer après chaque session.
- Ajouter les type hints en même temps que le code, pas après.
- Ne pas utiliser `# type: ignore` sans raison documentée.
- Viser mypy strict (`--strict`) optionnellement pour anticiper.

**Indicateur d'alerte** : Plus de 20 erreurs mypy à la fin de S05.

---

### :red_circle: R04 — Build PyInstaller défaillant

**Description** : PyInstaller peut échouer à embarquer les assets Arcade (images, sons, polices) ou produire un binaire non fonctionnel sur la plateforme cible.

**Mitigation** :
- Tester le build dès S07, pas seulement en S09.
- Utiliser `--add-data` pour embarquer les assets explicitement.
- Tester le binaire produit dans un environnement propre (sans le venv de dev).
- Prévoir un plan B : distribuer via un zip avec instructions `pip install + python3`.

**Indicateur d'alerte** : Le binaire plante au lancement lors du premier test en S07.

---

### :large_orange_circle: R05 — Retard sur le Core gameplay

**Description** : Le moteur de jeu (boucle, collisions, fantômes) est la partie la plus complexe. Un retard ici décale toutes les phases suivantes.

**Mitigation** :
- Livrer un MVP minimal à la fin de S05 (joueur qui se déplace, pacgums collectés, fantômes qui bougent).
- Ne pas sur-ingénier l'IA des fantômes en premier : commencer par un mouvement aléatoire valide, affiner ensuite.
- Points de synchro bi-hebdomadaires pour détecter les retards tôt.

**Indicateur d'alerte** : Pas de labyrinthe rendu à l'écran à la fin de S03.

---

### :large_orange_circle: R06 — Incompatibilité Arcade chez l'évaluateur

**Description** : Python Arcade nécessite OpenGL 3.3+. Certaines machines de l'école ou VMs peuvent ne pas le supporter.

**Mitigation** :
- Tester sur une machine différente de celle de développement dès S05.
- Documenter les prérequis système dans le README et dans le build.
- Prévoir le packaging comme solution principale (build standalone qui embarque les dépendances).

**Indicateur d'alerte** : Erreur OpenGL lors du test sur une machine école.

---

### :large_orange_circle: R08 — Traceback visible pendant la soutenance

**Description** : Une exception non interceptée lors de la démo (config modifiée, fichier manquant, erreur de générateur) = pénalité directe selon le sujet.

**Mitigation** :
- Convention d'équipe : tout `except` doit logger un message clair ET continuer proprement.
- Passer en revue tous les `except Exception` génériques avant S08.
- Tester les scénarios d'erreur dans le TEST_PLAN.

---

### :large_yellow_circle: R07 — Mode triche incomplet

**Description** : Le mode triche est explicitement évalué lors de la peer review. Une fonctionnalité manquante ou buguée est visible immédiatement.

**Mitigation** :
- Lister toutes les fonctions triche dès S06 et les tester une par une avec le TEST_PLAN.
- Prévoir une interface claire pour activer chaque fonction (touches dédiées documentées).

---

### :large_yellow_circle: R09 — Indisponibilité d'un membre

**Description** : Maladie, examens, contraintes personnelles sur une semaine clé.

**Mitigation** :
- Les deux membres connaissent l'ensemble du code (revue croisée systématique).
- Pas de "silo" : aucun module ne doit être compris par un seul membre.
- Prévoir du slack dans le planning (les phases 1 et 2 ont de la marge).

---

### :large_green_circle: R10 — Highscores corrompus

**Description** : Le fichier JSON des highscores peut être absent, vide, ou mal formé.

**Mitigation** :
- `ScoreManager` doit gérer tous ces cas : fichier absent → créer un nouveau, contenu invalide → réinitialiser proprement avec log.
- Tester explicitement ces cas dans les tests unitaires.

---

## Suivi des risques

> Mettre à jour chaque semaine.

| ID | Statut actuel | Évolution | Notes |
|---|---|---|---|
| R01 | :large_yellow_circle: En surveillance | — | Package reçu, à tester |
| R02 | :large_yellow_circle: En surveillance | — | |
| R03 | :large_yellow_circle: En surveillance | — | |
| R04 | :large_yellow_circle: En surveillance | — | |
| R05 | :large_yellow_circle: En surveillance | — | |
| R06 | :large_yellow_circle: En surveillance | — | |
| R07 | :large_yellow_circle: En surveillance | — | |
| R08 | :large_yellow_circle: En surveillance | — | |
| R09 | :large_green_circle: Faible | — | |

---

*Dernière mise à jour : 29/04/2026*